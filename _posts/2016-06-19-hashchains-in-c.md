---
layout: post
title: Authentication with Hash Chains in C
description: Buffers and chains and crypto, oh my!
---

One of my silliest long-running projects is a chatbot called [cbot][]. All it
does is connect to an IRC (Internet Relay Chat) server, and respond to people's
messages. For instance, if you greet it, it will greet you back. If you insult
it, it will send you a poorly-constructed comeback. Obviously there's nothing
groundbreaking about it - there are other chatbots that are much better. I made
cbot because I wanted to learn some new concepts (specifically the IRC protocol
and dynamic loading), and it was really helpful for that purpose. Plus, it's
another project in C, and I like projects in C!

I've been tinkering with cbot lately, and I realized that I wanted to add some
commands that only I can run. For instance, making it switch channels or leave
IRC. Or even change its nickname. The problem was that I didn't have a good way
to authenticate myself. I can't just whitelist my IRC nickname, because anyone
can change their nickname - if I disconnected, someone could steal my nickname
and control my bot. So I started brainstorming some more, uh, "elaborate"
solutions to this problem.

Today I came up with a solution I think is pretty great: hash chains!

## What's a hash chain?

In computer science, we have a concept of a "cryptographic hash function". They
sound complicated (and they are), but their concepts are simple. The idea is
that they should take some data as input and produce a big number---a
"hash"---as output. The important thing is that it should be very difficult for
somebody to figure out what the input data was for a given hash.

In a hash chain, you simply start with a number, and you hash it. Then, you hash
the result. Then you hash *that* result. You end up getting a sequence of hash
values like this:

    seed = some number
    hash_0 = H(seed)
    hash_1 = H(hash_0)
    hash_2 = H(hash_1)
    ...
    hash_n = H(hash_n-1)
    
If someone were to give you `hash_n-1` and `hash_n`, it would be easy for you to
verify that they are part of the same hash chain. You'd just have to make sure
that `H(hash_n-1)` was equal to `hash_n`. But if somebody gave you `hash_n` and
nothing else, it would be impossible for you to figure out any of the previous
hash values in this chain.

## Hash chains for authentication

So how can we use this to authenticate my commands to cbot? It's quite simple.
First, we generate a big, long hash chain. Maybe 1000 hashes in the chain. We
keep the seed of that chain a secret. Or, we randomly generate it and forget
about it. It doesn't matter too much.

What does matter is that we keep a copy of the whole hash chain somewhere safe.

Then, we give cbot a single hash value: `hash_1000` in this case. Cbot hangs
onto this in memory, and whenever I want to give it a command, I give it
`hash_999` as "proof" of my identity. To verify it, cbot does two things:

1. Verify that `H(hash_999)` equals `hash_1000`.
2. Replace `hash_1000` with `hash_999` in memory.

Next time I give a command, I verify my identity with `hash_998`, and so on. At
some point, I'll have to instruct CBot to start with a new hash chain, but that
isn't difficult at all.

The nice thing about this is that I can give commands and authentication to CBot
in a public channel. There can be a whole bunch of people listening in, but they
won't be able to figure out the next "password", and they won't be able to reuse
previous passwords to send commands to CBot.

## Implementation

So how can we implement this in C? Well, there's one rule you should always
follow in the world of cryptography: *never do it yourself.* Cryptography is
very difficult to implement, so you should let somebody smarter than you
implement it. So instead of trying to implement a hash function ourselves, we'll
use a handy library called OpenSSL, which happens to have a huge variety of
cryptographic hash functions already implemented.

The downside of using OpenSSL is that it has pretty bad documentation. All of
the documentation is in man pages, and they seem to be missing lots of
information.  So I'll walk through how I got OpenSSL to do my bidding.

I haven't yet implemented this authentication process into CBot, so instead I'll
describe my implementation of a command line program, [hashchain][], that does
the basic operations required.

### Creating a Hash Chain

OpenSSL's main interface for using its cryptography library is through the `EVP`
functions. These let you do common operations (like creating message digests,
more commonly known as hashes) in a way that abstracts away the particular
algorithm. So when you use OpenSSL's `EVP_MD` functions, you can easily swap out
the MD5 hash algorithm for SHA256. I even made it a command line argument!

Now let's get down to some code. We'll represent a hash chain with the following
struct:

```c
struct hash_chain {
  int digest_size;
  int chain_length;
  uint8_t *data;
};
```

And here is a function that will actually create a hash chain. It takes as an
argument some seed data (`base` along with `baselen`), a hash algorithm
specified by the argument `type`, and the length of the chain.

```c
struct hash_chain hash_chain_create(void *base, int baselen, const EVP_MD *type,
                                    int chain_len)
{
  EVP_MD_CTX *ctx;
  struct hash_chain output;
  uint32_t idx = 0;

  // Allocate space for our hash chain.
  output.digest_size = EVP_MD_size(type);
  output.chain_length = chain_len;
  output.data = calloc(output.chain_length, output.digest_size);

  // Hash the base data.
  ctx = EVP_MD_CTX_create();
  EVP_DigestInit_ex(ctx, type, NULL);
  EVP_DigestUpdate(ctx, base, baselen);
  EVP_DigestFinal_ex(ctx, output.data, NULL);

  // For each remaining item in the chain, hash the previous digest.
  for (idx = 1; idx < (uint16_t)output.chain_length; idx++) {
    EVP_DigestInit_ex(ctx, type, NULL);
    EVP_DigestUpdate(ctx, output.data + (idx - 1) * output.digest_size,
                     output.digest_size);
    EVP_DigestFinal_ex(ctx, output.data + idx * output.digest_size, NULL);
  }

  // Cleanup and return the chain.
  EVP_MD_CTX_destroy(ctx);
  return output;
}
```

The meat of this function is the calls to the `EVP_` functions. Here's how they
work: To start using the `EVP_MD` functions, you need a context object, which is
of type `EVP_MD_CTX`. You can get a pointer to one by calling
`EVP_MD_CTX_create()`, and destroy it using `EVP_MD_CTX_destroy()`. Next you
have to tell your context object which algorithm you'll be using by calling
`EVP_DigestInit_ex()`. We took our algorithm as the argument `type`, so this is
easy. The last argument can even specify an implementation for that algorithm,
but we want to use the default implementation OpenSSL comes with. Then, you hash
your data by calling `EVP_DigestUpdate()` with a pointer to the data to hash
(and its length). You can get the actual hash value out of the context by
calling `EVP_DigestFinal_ex()` with a pointer to where you want the data
written.

You can see that this process is done twice in this function. The first time
hashes the input data into the output buffer. The second time is within the for
loop, where we simply keep hashing the previous data into the next hash slot.

### Verifying A Hash

The code for verifying a hash should be simple, given that we have just seen how
to compute a hash using OpenSSL. Here is a function that verifies that `h`
hashes to `tip`, using the hash algorithm `hash`:

```c
bool hash_chain_verify(const void *h, const void *tip, const EVP_MD *hash)
{
  EVP_MD_CTX *ctx;
  int result;
  int digest_len = EVP_MD_size(hash);
  void *data = malloc(digest_len);

  ctx = EVP_MD_CTX_create();
  EVP_DigestInit_ex(ctx, hash, NULL);
  EVP_DigestUpdate(ctx, h, digest_len);
  EVP_DigestFinal_ex(ctx, data, NULL);
  EVP_MD_CTX_destroy(ctx);

  result = memcmp(data, tip, digest_len);
  free(data);

  return result == 0;
}
```

You can see that once more, we're doing the same create, init, update, final,
and destroy pattern. The major difference being that afterwards, we're using
`memcmp()` to ensure that the resulting hash of `h` is the same as `tip`.

### Implementation Details: base64

In order to use these functions in a command line tool, we need to be able to
output and read in our hashes. Unfortunately, hashes are just binary data, and
they don't look too pretty if you were to try to print them on the console. To
solve this, we use base64 encoding.  It's a way of representing binary data using only the characters A-Z, a-z, 0-9, `/`, and `-`.

The good news is that OpenSSL has base64 encoding implemented. The bad news is
that this means we need to figure out more of OpenSSL's API.

A little searching reveals that OpenSSL has an abstraction for input and output
called `BIO`. The idea is somewhat similar to Unix pipes. You have `BIO` objects
that can produce data, some that consume data, and some that can `filter` data.
For example, files can produce or consume data, while base64 is simply a filter:
something that takes input data and changes the way it's represented. So here is
how we combine OpenSSL's base64 `BIO` with `stdout` to be able to print every
hash value in a hash chain:

```c
void hash_chain_print(struct hash_chain chain, FILE *f)
{
  BIO *out, *b64, *bio;
  b64 = BIO_new(BIO_f_base64());
  out = BIO_new_fp(f, BIO_NOCLOSE);
  bio = BIO_push(b64, out);

  for (int i = 0; i < chain.chain_length; i++) {
    BIO_write(bio, chain.data + i * chain.digest_size, chain.digest_size);
    BIO_flush(bio);
  }

  BIO_free_all(bio);
}
```

First, we create a base64 `BIO` object, along with another one which will write
to file `f`. We use `BIO_push()` to hook up the output of `b64` to the input of
`out`. Next, we go through each hash in the chain and call `BIO_write()`, which
pushes the data *through* the base64 encoder and out into the file.
`BIO_flush()` tells the base64 encoder that it should write out the data it's
gotten so far on a line, so that each hash value gets its own line.

Similarly, we need to be able to take base64 encoded data as input and convert
it to bytes. For that, we have to do a reversed task: instead of *writing* data
into a base64 encoder, we *read* it through the base64 encoder. In this case we
also make use of the fact that OpenSSL lets us use an arbitrary buffer as a
`BIO` as well. The following is a function that decodes a base64 encoded string,
given that you know the original data's length:

```c
void *base64_decode(char *str, int explen)
{
  uint8_t *buf = malloc(explen);
  BIO *b = BIO_new_mem_buf(str, -1);
  BIO *b64 = BIO_new(BIO_f_base64());
  BIO_push(b64, b);
  BIO_set_flags(b64, BIO_FLAGS_BASE64_NO_NL);
  BIO_read(b64, buf, explen);
  BIO_free_all(b64);
  return buf;
}
```

First, we allocate a buffer to hold our decoded data. Then, we wrap the input
string in a `BIO` object, and we again create a base64 `bio` object. We combine
the two `BIO`s together. One important thing here is that it seems like the
base64 decoder normally waits for a newline before it decodes all of the data
you read. We don't want this behavior, since our input data doesn't have a
newline. So, we tell it not to wait for a newline with the
`BIO_FLAGS_BASE64_NO_NL` flag (this was not documented by OpenSSL at all -
thanks to [this article](http://doctrina.org/Base64-With-OpenSSL-C-API.html) for
the info!).

Once all that is done, we simply need to read data through the `BIO` chain into
our buffer, and return it back to the caller.

### Putting it together

From these four functions, I was able to put together a small command line
program that can create and verify hash chains. I won't bother copying down the
driver code for this program, but you can find it at [GitHub][hashchain]. The
end product can be used something like this:

    $ ./hashchain create sha256 20 "secret seed here" > chain
    $ tail -n 2 chain
    gjZmdTdMNnijpZd0hhkxJSK9/IywQIQ2H5N2BiWC6w0=
    5o/+3BTbOTebzIJGTI0bZPorFatbV1zu070qBSx3Z0k=
    $ ./hashchain verify gjZmdTdMNnijpZd0hhkxJSK9/IywQIQ2H5N2BiWC6w0= 5o/+3BTbOTebzIJGTI0bZPorFatbV1zu070qBSx3Z0k=
    success
    $ ./hashchain verify not-really-a-valid-hash-at-all-1234567890ab= 5o/+3BTbOTebzIJGTI0bZPorFatbV1zu070qBSx3Z0k=
    failure

## Conclusion

From this quick implementation with OpenSSL, we can see that it's not too
difficult to create hash chains and verify hashes when we receive them. It's not
too much of a leap to see how I could apply this to my IRC bot - and I'm sure I
will soon. Of course, this probably isn't the best way to do command
authentication on IRC - but it's interesting and the implementation was fun!

[cbot]: https://github.com/brenns10/cbot
[hashchain]: https://github.com/brenns10/hashchain
