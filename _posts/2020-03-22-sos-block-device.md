---
layout: post
title: "Implementing a virtio-blk driver in my own operating system"
description: "Implementing a virtio-blk driver in my own operating system"
---

In this blog post, I'm going to describe how I wrote my first block device
driver in my operating system, SOS. This OS is my personal project for exploring
how to implement an operating system.  You can find more inforation about it in
my [first post][sos-preempt] about SOS, or check it out on [Github][sos-gh].

I think it's important to note that I'm not an expert at device drivers, and I'm
not trying to demonstrate the best way to implement this. This just presents my
journey through my first implementation, in the hopes that other people are
interested in learning more about what an OS does. So, with all that said, I'm
just going to jump in!

### What is a block device?

Loosely speaking, a block device is a hard drive, SD card, or any other device
which stores a lot of data. These devices can store far more data than main
memory, but loading and storing it takes a long time compared to registers,
cache, or memory.  They index and store their data in "blocks". For example,
the block device I worked with organized its data into sectors of 512 bytes. To
load bytes 0-511, you load sector 0, to read bytes 512-1023, you load sector 1,
etc.

Applications don't typically work in terms of blocks or sectors. Instead, they
think in terms of files and file paths. The filesystem allows applications to
ask to read or write a sequence of bytes, without knowing anything about how the
blocks are organized, or even what device is used to store the files. This
article is not going to get into implementing the filesystem. Instead, we will
just focus on reading and writing blocks of data, which allows a file system to
be implemented later. As soon as I implement a file system, I hope to write an
article about it!

### What kind of block device?

My operating system targets ARMv7-A, and its reference platform is the QEMU
"virt" machine. Although there are many types of block device interfaces, I
chose to implement a simple one which doesn't exist on real hardware, the
virtio-blk device. This device is specified in the [Virtio 1.0][virtio]
specification, which specifies an entire family of device types. The intent of
virtio devices is to be implemented by hypervisors (such as QEMU). They simplify
things a bit, so that it's easier and more efficient for hypervisors and guests
to communicate, without having to emulate any quirks of real hardware devices.
Strangely enough, there's even some movement on making _real devices_ which
implement the virtio interfaces (see this [LWN
article][lwn-virtio-without-virt]). However, the primary goal is definitely for
use with virtual machines.

It may seem silly to consider this a block device driver implementation, given
that it's just for a "made-up" virtual hard disk. But since a VM is my best
platform for development, all device drivers I implement will have to be for
fake devices anyway. As a result, I think that working with the virtio devices
is the most straightforward way to do this.

### Finding and accessing a virtio device

The first step of getting a device driver to work is to detect whether that
device even exists on the current machine. ARM machines generally use [Device
Tree][dtree] to enumerate devices, and QEMU is no different. While SOS does
implement some parsing for device trees, right now the implementation is not at
the point where it can dynamically load device drivers. So I manually took a
look at the device tree, and noticed these entries:

```
  virtio_mmio@a000000 {
    dma-coherent;
    interrupts = <0x00 0x10 0x01>;
    reg = <0x00 0xa000000 0x00 0x200>;
    compatible = "virtio,mmio";
  };

  virtio_mmio@a000200 {
    dma-coherent;
    interrupts = <0x00 0x11 0x01>;
    reg = <0x00 0xa000200 0x00 0x200>;
    compatible = "virtio,mmio";
  };

  ...
```

These entries continue on for a while; there are a total of 32 of them
stretching from memory lcation 0x0A000000 to 0x0A004000. The "mmio" portion
stands for Memory Mapped I/O, which means that all of the registers for these
devices appear simply as memory addresses. This is different from the [timer
driver][sos-preempt] which I implemented in my last article, which used
special ARM instructions to read and write the device registers.

Since these devices are memory-mapped, this means we can write structs which
represent the device registers, to make things much simpler in C. Here is the
structure I use to represent every virtio-mmio device in SOS, based on Section
4.2.2 of the [spec][virtio]:

```c
typedef volatile struct __attribute__((packed)) {
	uint32_t MagicValue;
	uint32_t Version;
	uint32_t DeviceID;
	uint32_t VendorID;
	uint32_t DeviceFeatures;
	uint32_t DeviceFeaturesSel;
	uint32_t _reserved0[2];
	uint32_t DriverFeatures;
	uint32_t DriverFeaturesSel;
	uint32_t _reserved1[2];
	uint32_t QueueSel;
	uint32_t QueueNumMax;
	uint32_t QueueNum;
	uint32_t _reserved2[2];
	uint32_t QueueReady;
	uint32_t _reserved3[2];
	uint32_t QueueNotify;
	uint32_t _reserved4[3];
	uint32_t InterruptStatus;
	uint32_t InterruptACK;
	uint32_t _reserved5[2];
	uint32_t Status;
	uint32_t _reserved6[3];
	uint32_t QueueDescLow;
	uint32_t QueueDescHigh;
	uint32_t _reserved7[2];
	uint32_t QueueAvailLow;
	uint32_t QueueAvailHigh;
	uint32_t _reserved8[2];
	uint32_t QueueUsedLow;
	uint32_t QueueUsedHigh;
	uint32_t _reserved9[21];
	uint32_t ConfigGeneration;
	uint32_t Config[0];
} virtio_regs;
```

This struct is really long, and as a reader you don't need to understand most of
it. All you really need to know is that, to get started, we can simply create a
pointer to this struct at the physical memory addresses mentioned in the device
tree. So let's examine the code to do this:

```c
void virtio_init(void)
{
	/* TODO: we know these addresses due to manually reading device tree,
	 * but we should automate that */
	uint32_t page_virt = alloc_pages(kern_virt_allocator, 0x4000, 0);
	kmem_map_pages(page_virt, 0x0a000000U, 0x4000, PRW_UNA | EXECUTE_NEVER);
	
	for (int i = 0; i < 32; i++)
		virtio_dev_init(page_virt + 0x200 * i, 32 + 0x10 + i);
}
```

The first step is a bit tricky, since SOS uses virtual memory. We first allocate
a virtual memory region large enough to hold all 32 entries in the device tree.
We then use my function `kmem_map_pages()`, which takes virtual and physical
addresses, and creates a mapping between them in the MMU's page tables. So, when
we access the (virtual) memory address at `page_virt`, the ARM MMU will
translate that into the physical memory address `0x0A000000`. After this point,
we simply iterate over every device, and call the `virtio_dev_init()` function,
which does per-device initialization.

The first argument to `virtio_dev_init()` should be reasonably self-explanatory;
it is the memory address of the device. However the second argument is
pretty weird. This argument is the *interrupt ID* of the device, which is
derived from the `interrupt` field in the device tree. I don't want to get too
bogged down in the details of ARM interrupt IDs, so let's gloss over that for
now. Instead, let's take a look at the per-device initialization:

```c
static int virtio_dev_init(uint32_t virt, uint32_t intid)
{
	virtio_regs *regs = (virtio_regs *) virt;

	if (READ32(regs->MagicValue) != VIRTIO_MAGIC) {
		printf("error: virtio at 0x%x had wrong magic value 0x%x, expected 0x%x\n",
				virt, regs->MagicValue, VIRTIO_MAGIC);
		return -1;
	}
	if (READ32(regs->Version) != VIRTIO_VERSION) {
		printf("error: virtio at 0x%x had wrong version 0x%x, expected 0x%x\n",
				virt, regs->Version, VIRTIO_VERSION);
		return -1;
	}
	if (READ32(regs->DeviceID) == 0) {
		/*On QEMU, this is pretty common, don't print a message */
		/*printf("warn: virtio at 0x%x has DeviceID=0, skipping\n", virt);*/
		return -1;
	}

	/* ... to be continued ... */
}
```

I broke this function up a bit so that we could examine it in parts. Our first
step is to take the address we are given (`virt`) and cast it into a pointer to
`virtio_regs`. Now we can begin accessing register fields of the device. The
first thing we check is the `MagicValue` register, which will always contain a
special number (`0x74726976` in case you were wondering, which forms the string
"virt"). This helps us guarantee that we're really looking at a virtio device,
because random memory would be very unlikely to contain that value.

But what is this `READ32()` business, and why are we using it? To answer this, I
need to do a short diversion into two things:

1. *Aligned access:* ARM assembly can use several instructions to access memory:
   `ldrb` loads a single byte, while `ldr` loads a full 4-byte word from memory.
   Real memory can handle any type of accesses, but the device drivers we're
   talking to are _not real memory_, they're just memory-mapped registers. It
   wouldn't make sense to read just one byte out of a 4-byte register, and so if
   your code asks to do that, the device (or memory bus?) won't be able to
   answer your request. The `READ32()` and `WRITE32()` macros try to ensure that
   the compiler only ever generates code which access the full 4-byte words.
2. *The `volatile` keyword:* C compilers use memory a lot, and they make a lot
   of assumptions about it. For instance, if you write some code like this:

   ```c
   uint32_t *x = malloc(sizeof(uint32_t));
   *x = 5;
   printf("the value pointed by x is %u\n", *x);
   ```

   The C compiler knows that you are saying to assign some random word of memory
   the value 5, and then print that word of memory out. But it knows that memory
   doesn't just change values randomly, and it also knows that memory access can
   be expensive. So rather than assigning 5 to that memory location, storing it,
   and then reading it back from memory, the compiler could very well just store
   5 to that memory address, and then print the value 5 out without bothering to
   read it back. Normally, this is a good optimization, but with memory-mapped
   peripherals, all these assumptions are wrong! It's totally possible that when
   you write 5 to a peripheral register, the peripheral could change it so that
   it reads back a different value. In that case, this C code would be wrong.

   To avoid this, C's `volatile` keyword allows us to instruct the compiler that
   memory values could change _at any time_, and so every time we ask to read a
   memory location, it should actually generate code to read from memory.

So, to summarize, `READ32()` instructs the compiler to always read a 4-byte
word, without doing any optimizations: always accessing directly from memory.
Getting back to the `virtio_dev_init()` function, we use this macro again to
read out the `Version` register, which we expect to contain the value 2, while
legacy devices contain the value 1. As it turns out, legacy devices are very
common even today. So common, in fact, that QEMU defaults to using legacy virtio
devices rather than the more recent virtio version. Since I only support the
most recent version, I had to spend at least an hour digging through mailing
lists and QEMU source code to find out the magic command line argument which
forces it to use version 2: `-global virtio-mmio.force-legacy=false`.

So now we're confident that the device is in fact a virtio, and we know that it
speaks the version of the protocol which we expect. So now, it's time to find
out just what kind of device this is, which we learn via the `DeviceID`
register. There are several types of virtio devices: network cards (ID 1) and
block devices (ID 2) are two such examples. It is also possible, however, that
this device is actually inactive, in which case the ID would be 0. This is
common for QEMU, which simply puts 32 inactive virtio devices into the machine,
and as you add devices such as hard disks, it activates individual devices. So,
our code handles this without printing any error message.

### Saying hello

Let's continue looking at the `virtio_dev_init()` function:

```c
static int virtio_dev_init(uint32_t virt, uint32_t intid)
{
	/* ... see above ... */

	/* First step of initialization: reset */
	WRITE32(regs->Status, 0);
	mb();
	/* Hello there, I see you */
	WRITE32(regs->Status, READ32(regs->Status) | VIRTIO_STATUS_ACKNOWLEDGE);
	mb();

	/* Hello, I am a driver for you */
	WRITE32(regs->Status, READ32(regs->Status) | VIRTIO_STATUS_DRIVER);
	mb();

	switch (READ32(regs->DeviceID)) {
	case VIRTIO_DEV_BLK:
		return virtio_blk_init(regs, intid);
	default:
		printf("unsupported virtio device ID 0x%x\n", READ32(regs->DeviceID));
	}
}
```

In this function, we do the first steps of initialization according to section
3.1 of the [virtio spec][virtio]. First, we reset the device by writing 0 to its
Status register. Then, we set an `ACKNOWLEDGE` bit which informs the device that
we've observed it, and then we set a `DRIVER` bit which states that we have a
driver for the device. Finally, we check the device type, and if the device is a
block device, we continue to `virtio_blk_init()`.

But what about these `mb()` function calls? These stand for "memory barrier",
and they get into another complexity of memory-mapped peripherals. Memory can be
cached by CPUs, to enable faster access. When you write a value to memory, your
update could have gone straight to cache, which means that the update is visible
to you, but maybe not to other devices on the memory bus yet. The `mb()`
function invokes the ARM `dsb` instruction, which asks the processor to wait
until all memory writes before it have become visible to all devices on the
system. There's actually quite a bit more complexity to this topic, and I can't
stress enough that I know very little about this. Almost certainly, I'm
simplifying and over-using memory barriers here.

So in the case that we've found ourselves a block device, what happens next?
Let's take a look at the first part of `virtio_blk_init()`:

```c
static int virtio_blk_init(virtio_regs *regs, uint32_t intid)
{
	volatile struct virtio_blk_config *conf = (struct virtio_blk_config*)regs->Config;
	struct virtqueue *virtq;
	uint32_t request_features = 0;
	uint32_t DeviceFeatures;
	uint32_t i;
	
	WRITE32(regs->DeviceFeaturesSel, 0);
	WRITE32(regs->DriverFeaturesSel, 0);
	mb();
	DeviceFeatures = regs->DeviceFeatures;
	virtio_check_capabilities(&DeviceFeatures, &request_features, blk_caps, nelem(blk_caps));
	virtio_check_capabilities(&DeviceFeatures, &request_features, indp_caps, nelem(indp_caps));

	if (DeviceFeatures) {
		printf("virtio supports undocumented options 0x%x!\n", DeviceFeatures);
	}

	WRITE32(regs->DriverFeatures, request_features);
	WRITE32(regs->Status, READ32(regs->Status) | VIRTIO_STATUS_FEATURES_OK);
	mb();
	if (!(regs->Status & VIRTIO_STATUS_FEATURES_OK)) {
		puts("error: virtio-blk did not accept our features\n");
		return -1;
	}

	/* ... to be continued ... */
}
```

In this section, we do what's called "feature negotiation". The virtio standard
defines several features which a device and driver can optionally support. The
driver reads what features the device supports, and selects the subset of
features it supports. If the device is missing a required feature, the driver
can report an error and stop. Similarly, if the driver selects a set of features
which the device can't support, then the device can reject the feature selection
too.

I wrote a fair amount of code for this, which ultimately does not do that much,
and so I'm electing not to include it in the article. To cut a long story short,
this code (mostly in `virtio_check_capabilities()`) reads out all the supported
features and prints them out. Since I didn't write any code to support any
extra features, at the end of the day I just tell the device that I don't want
any extra features, and check if the driver reported an error.

Now that feature negotiation is set aside, let's look at what comes next:

```c
static int virtio_blk_init(virtio_regs *regs, uint32_t intid)
{
	volatile struct virtio_blk_config *conf = (struct virtio_blk_config*)regs->Config;
	/* ... see above ... */

	printf("virtio-blk has 0x%x %x sectors\n", HI32(conf->capacity), LO32(conf->capacity));
	printf("virtio-blk queuenummax %u\n", READ32(regs->QueueNumMax));
	printf("virtio-blk Status %x\n", READ32(regs->Status));
	printf("virtio-blk InterruptStatus %x\n", regs->InterruptStatus);

	virtq = virtq_create(128);
	virtq_add_to_device(regs, virtq, 0);

	blkdev.regs = regs;
	blkdev.virtq = virtq;
	blkdev.intid = intid;

	gic_register_isr(intid, 1, virtio_blk_isr);
	gic_enable_interrupt(intid);

	WRITE32(regs->Status, READ32(regs->Status) | VIRTIO_STATUS_DRIVER_OK);
	mb();
	printf("virtio-blk Status %x\n", READ32(regs->Status));

	maybe_init_blkreq_slab();
	printf("virtio-blk 0x%x (intid %u): ready!\n", kmem_lookup_phys((void*)regs), intid);
}
```

Now, we print out some information from the `virtio_blk_config` structure, which
is similar to the `virtio_regs` structure I created before. Block devices can
report all sorts of information in this configuration struct based on the
features we negotiated earlier. But since I didn't enable any features, the only
information we can read is the "capacity" value, which is a 64-bit number
represtenting the number of 512 byte sectors this device has. To simplify, I'll
exclude the definition of this structure, since it contains only that field.

We also print out some registers from the `virtio_regs` structure, which have to
do with the "virtqueue" we'll use to communicate with the device shortly. And
next, we use `virtq_create(128)` to create one of these objects (with capacity
128), and we use `virtq_add_to_device()` to inform the device of the memory
location for this virtqueue. (Don't worry, I'll explain what all this means in a
moment).

Next, we assign some fields of a `blkdev` structure: we save the `regs` pointer,
the `virtq` we just created, and the interrupt identifier which we were told
belongs to this device. In a more mature implementation, we would dynamically
allocate a structure to represent this device, but since this is preliminary, I
went ahead and just statically allocated one.

Next, we ask our interrupt controller to register an interrupt service routine,
so that `virtio_blk_isr()` gets called every time our interrupt ID is triggered.
We go ahead and enable the interrupt now. Finally, we tell the device that we've
done all of its initialization, and that it is ready to operate. And at the very
end, we use `maybe_init_blkreq_slab()` to initialize a memory allocator, which
we will use to allocate "block requests" which we'll send to, and receive from,
the driver.

### What's all this virtqueue nonsense??

Okay, so I've kept you in suspense long enough. In the last section I kept
talking about virtqueues and block requests, without explaining what they are.
The way that this device works is that we, the driver, will send requests to the
device. A read request ("IN" according to the virtio-blk terminology) will ask
the device to send us the contents of a single sector. A write request ("OUT")
will ask the device to write whatever we provided to the disk. A request looks
roughly like this (taken with some modification from section 5.2.6 of [the
virtio spec][virtio]):

```c
struct virtio_blk_req {
        uint32_t type;
        uint32_t reserved;
        uint64_t sector;
        uint8_t  data[512];
        uint8_t  status;
};
```

When we ask to read, we send a structure like this to the device, and the device
fills out `data` for us. When we ask for a write, we fill out `data` and send it
to the device. When the request is finished, the device triggers an interrupt,
and hands the structure back to us, with `status` filled out to let us know how
it went.

This all sounds pretty simple, but so far we haven't seen any good way to send
requests to the device. At first, you might think that we could just write the
address of this structure into a memory-mapped register, something like this:

```c
WRITE32(regs->HereIsARequestForYou, address_of_virtio_blk_req);
```

This would actually complicate things for the device. It would need to track all
of the requests it received, and presumably it would need some way of telling us
that it couldn't handle any more requests until it completed some of them, since
these devices aren't exactly fast. So instead, the virtio standard specifies a
data structure called a "virtqueue".

A virtqueue is a single direction queue which allows us to send blocks of memory
(like the `virtio_blk_req` shown above) to the device, and have it return the
memory to us once it has done some processing. The block device only needs one
virtqueue (which handles read and write requests). However, other types of
devices (like network cards) can have multiple virtqueues for different types of
requests.

The virtqueue has fixed size, and the driver is responsible for almost all
upkeep of the virtqueue, except for when the device updates a counter to inform
us that it has finished processing something.

### What does a virtqueue look like?

A virtqueue is basically three arrays and some counters. The first array holds
what we call "descriptors". Here is the struct I use to represent a single
descriptor in the array:

```c
struct virtqueue_desc {
	uint64_t addr;
	uint32_t len;
/* This marks a buffer as continuing via the next field. */
#define VIRTQ_DESC_F_NEXT   1
/* This marks a buffer as device write-only (otherwise device read-only). */
#define VIRTQ_DESC_F_WRITE     2
/* This means the buffer contains a list of buffer descriptors. */
#define VIRTQ_DESC_F_INDIRECT   4
	/* The flags as indicated above. */
	uint16_t flags;
	/* Next field if flags & NEXT */
	uint16_t next;
} __attribute__((packed));
```

Each descriptor contains a physical memory address, which points to the memory
buffer we are sending to the device, and a length, telling how long the buffer
is. The descriptor contains some additional metadata, including a `WRITE` flag
telling the device whether it has permission to write to this memory. The
descriptor also contains a `NEXT` flag and `next` field. This lets us create a
request for the device which is actually made up of several descriptors in a
chain. We'll see why this is useful in a moment.

The second array in a virtqueue is called the `avail` array. We use this struct
to represent the full array, and some metadata:

```c
struct virtqueue_avail {
#define VIRTQ_AVAIL_F_NO_INTERRUPT 1
	uint16_t flags;
	uint16_t idx;
	uint16_t ring[0];
} __attribute__((packed));
```

The `avail` array is where we, the driver, insert requests we want to make
"available" to the device. The `idx` field here tracks where we will place the
next request. The `ring` array here is the actual array, and it contains 16-bit
descriptor indexes.

So, if the driver wants to send a block of memory to the device, it will first
create a descriptor which has that buffer's information. Then, it will insert
that descriptor's index into the `ring` array on the `avail` structure, at
`idx`. Finally, it will increment `idx`, and _notify_ the device that it has
updated the queue, simply by writing to a device register.

The final array in the virtq is called the `used` array. We use these structs to
represent it:

```c
struct virtqueue_used_elem {
	uint32_t id;
	uint32_t len;
} __attribute__((packed));

struct virtqueue_used {
#define VIRTQ_USED_F_NO_NOTIFY 1
	uint16_t flags;
	uint16_t idx;
	struct virtqueue_used_elem ring[0];
} __attribute__((packed));
```

This array is where the driver will place the descriptors which it is finished
processing. Once it has handled a request, it will take the descriptor (which
could be a chain, as we mentioned above), and its total length in bytes, and
write it into the `ring` array at index `idx`. Then, the device updates `idx`
and sends us an interrupt.

Altogether, I use the following struct to manage the entire virtqueue:

```c
struct virtqueue {
	/* Physical base address of the full data structure. */
	uint32_t phys;
	uint32_t len;
	uint32_t seen_used;
	uint32_t free_desc;

	volatile struct virtqueue_desc *desc;
	volatile struct virtqueue_avail *avail;
	volatile uint16_t *used_event;
	volatile struct virtqueue_used *used;
	volatile uint16_t *avail_event;
	void **desc_virt;
} __attribute__((packed));
```

`phys` is the physical address of this structure, and `len` is the number of
slots in each array. `seen_used` is a field which lets the driver track the last
`idx` it saw in the `used` array, so that it knows how many new responses it has
received since last time. And `free_desc` helps us track which descriptors are
available for our use when we want to send a new command.

The pointers `desc`, `avail`, and `used` point to the arrays we described above,
and `used_event` and `avail_event` are related to extension features you can
negotiate during initialization. We won't talk about them.

Finally, we have the `desc_virt` pointer. This points to a fourth array which
we need to maintain on our own. Although the device can only understand physical
addresses, our driver needs to know the virtual addresses which corresponds to
each descriptor. We can't just look up the virtual address which maps to a
physical address, so we have to store that data in this array.

### Using the virtio-blk virtqueue

My `virtq_create()` function (used way above) will allocate a page of memory and
lay out all of these arrays and structures within it. The function needs to take
into account the sizes of all the arrays, as well as alignment requirements. As
such, it's a bit dense, and I'm going to omit it from the article. But with all
of the description above, you shouldn't really need to see this part anyway.
What I do want to show here is the `virtq_add_to_device()` function.

```c
void virtq_add_to_device(volatile virtio_regs *regs, struct virtqueue *virtq, uint32_t queue_sel)
{
	WRITE32(regs->QueueSel, queue_sel);
	mb();
	WRITE32(regs->QueueNum, virtq->len);
	WRITE32(regs->QueueDescLow, virtq->phys + ((void*)virtq->desc - (void*)virtq));
	WRITE32(regs->QueueDescHigh, 0);
	WRITE32(regs->QueueAvailLow, virtq->phys + ((void*)virtq->avail - (void*)virtq));
	WRITE32(regs->QueueAvailHigh, 0);
	WRITE32(regs->QueueUsedLow, virtq->phys + ((void*)virtq->used - (void*)virtq));
	WRITE32(regs->QueueUsedHigh, 0);
	mb();
	WRITE32(regs->QueueReady, 1);
}
```

Since a device could have many more than just one virtqueue, they are indexed
starting at 0. The `queue_sel` parameter specifies which virtqueue we're talking
about. Our first step is writing this number to the `QueueSel` register.
Whenever you write to any of the other `Queue` registers, the device consults
the `QueueSel` register to know which queue we're configuring. So it's important
to explicitly select the correct one! Then, we set the 64-bit physical addresses
of each array in the queue, and set the length of the queue in the `QueueNum`
register. Finally, we write 1 into `QueueReady`, telling the device that it can
start using the queue.

### Reading and Writing, oh my!

At this point, we've thoroughly discussed the initialization steps of the
driver. We've negotiated features, allocated a queue to transmit requests, and
attached it to the driver. We are now ready to see how the driver uses all of
this to implement the read and write commands. If you've made it this far,
thanks for sticking with me!

We can implement both read and write in a single function, which takes the
operation type (IN or OUT), the sector number, and a pointer to data we'll read
or write to:

```c
static int virtio_blk_cmd(struct virtio_blk *blk, uint32_t type, uint32_t sector, uint8_t *data)
{
	struct virtio_blk_req *hdr = slab_alloc(blkreq_slab);
	uint32_t d1, d2, d3, datamode = 0;

	hdr->type = type;
	hdr->sector = sector;

	d1 = virtq_alloc_desc(blk->virtq, hdr);
	blk->virtq->desc[d1].len = VIRTIO_BLK_REQ_HEADER_SIZE;
	blk->virtq->desc[d1].flags = VIRTQ_DESC_F_NEXT;
	
	if (type == VIRTIO_BLK_T_IN) /* if it's a read */
	 datamode = VIRTQ_DESC_F_WRITE; /* mark page writeable */

	d2 = virtq_alloc_desc(blk->virtq, data);
	blk->virtq->desc[d2].len = VIRTIO_BLK_SECTOR_SIZE;
	blk->virtq->desc[d2].flags = datamode | VIRTQ_DESC_F_NEXT;

	d3 = virtq_alloc_desc(blk->virtq, (void*)hdr + VIRTIO_BLK_REQ_HEADER_SIZE);
	blk->virtq->desc[d3].len = VIRTIO_BLK_REQ_FOOTER_SIZE;
	blk->virtq->desc[d3].flags = VIRTQ_DESC_F_WRITE;

	blk->virtq->desc[d1].next = d2;
	blk->virtq->desc[d2].next = d3;

	blk->virtq->avail->ring[blk->virtq->avail->idx] = d1;
	mb();
	blk->virtq->avail->idx += 1;
	mb();
	WRITE32(blk->regs->QueueNotify, 0);
}
```

The first thing we do is allocate ourselves a `struct virtio_blk_req` structure
from the slab allocator we initialized earlier. The `virtio_blk_req` structure
looks very similar to the one which I showed earlier from the specification, but
with one major difference:

```c
struct virtio_blk_req {
#define VIRTIO_BLK_T_IN       0
#define VIRTIO_BLK_T_OUT      1
	uint32_t type;
	uint32_t reserved;
	uint64_t sector;
	/* NO DATA INCLUDED HERE! */
	uint8_t status;
} __attribute__((packed));
```

The reason here is simple. We would like to be able to read and write data
without having to copy it back and forth. If the data is embedded within the
`virtio_blk_req` structure, then we will have to copy the data out when we want
to send data up to the filesystem or to an application. So, we take advantage of
the fact that virtqueues allow us to chain descriptors. Rather than sending a
single descriptor to the device for each request, we send a chain of three:

1. The first is 16 bytes long, containing `type`, `reserved`, and `sector`. This
   descriptor is read-only.
2. The second is 512 bytes long, pointing to a completely different memory
   address (`data` which was passed into the function). This descriptor is
   device writeable.
3. The third is 1 byte long, pointing at the end of the `virtio_blk_req`
   structure, where the device can write the status information.

In fact, this approach is not only optimal, but it seems that it is very nearly
required. Descriptors must be either read-only or write-only for the device. And
it turns out that the spec requires that all read-only descriptors come first in
the chain, and all write-only descriptors come after it. I didn't realize this
at first, and encountered some errors from QEMU. Those errors sent me to stack
overflow, where I encountered some hero's [self-answered question][so], where
they encountered this same issue, and suggested the three-descriptor approach.

This is something which I think really ought to be spelled out by the
specification, but as far as I can tell they never give an example.

So, looking back at the `virtio_blk_cmd()` function, it should make a lot more
sense. We allocate that `virtio_blk_req` structure, and fill out the request
type and sector. Then, we create three descriptors (`virtio_alloc_desc()` uses
that `desc_free` variable along with the `next` pointers to track a big chain of
free descriptor indexes). We populate each descriptor's flags and length, and
link them all together to form one chain. Finally, we stick that descriptor
chain into the `avail` array and we notify the device.

The only major difference between reading and writing is the permission on the
second buffer, and the type of request we're making. Of course, when we write,
we don't particularly care about the response from the device (as long as it is
successful). On the other hand, when we read, the whole point is to fill out the
data pointer. To see the results of each request, we need to look at the
interrupt handler for this device:

```c
static void virtio_blk_isr(uint32_t intid)
{
	/* TODO: support multiple block devices by examining intid */
	struct virtio_blk *dev = &blkdev;
	int i;
	int len = dev->virtq->len;

	WRITE32(dev->regs->InterruptACK, READ32(dev->regs->InterruptStatus));

	for (i = dev->virtq->seen_used; i != dev->virtq->used->idx; i = wrap(i + 1, len)) {
		virtio_blk_handle_used(dev, i);
	}
	dev->virtq->seen_used = dev->virtq->used->idx;

	gic_end_interrupt(intid);
}
```

This ISR first acknowledeges the interrupt with the virtio device (otherwise the
interrupt will keep getting triggered). Then, it iterates over the items in the
`used` array which we haven't seen yet (making sure to wrap `idx` if it goes
past `len`). For each of these items, we call `virtio_blk_handle_used()`, and at
the end we update the "last seen" index, and end the interrupt.

Let's look at how we handle each used descriptor chain:

```c
static void virtio_blk_handle_used(struct virtio_blk *dev, uint32_t usedidx)
{
	struct virtqueue *virtq = dev->virtq;
	uint32_t desc1, desc2, desc3;
	struct virtio_blk_req *req;
	uint8_t *data;

	desc1 = virtq->used->ring[usedidx].id;
	if (!(virtq->desc[desc1].flags & VIRTQ_DESC_F_NEXT))
		goto bad_desc;
	desc2 = virtq->desc[desc1].next;
	if (!(virtq->desc[desc2].flags & VIRTQ_DESC_F_NEXT))
		goto bad_desc;
	desc3 = virtq->desc[desc2].next;
	if (virtq->desc[desc1].len != VIRTIO_BLK_REQ_HEADER_SIZE
			|| virtq->desc[desc2].len != VIRTIO_BLK_SECTOR_SIZE
			|| virtq->desc[desc3].len != VIRTIO_BLK_REQ_FOOTER_SIZE)
		goto bad_desc;

	req = virtq->desc_virt[desc1];
	data = virtq->desc_virt[desc2];
	if (req->status != VIRTIO_BLK_S_OK)
		goto bad_status;
	
	if (req->type == VIRTIO_BLK_T_IN) {
		printf("virtio-blk: result: \"%s\"\n", data);
	}

	virtq_free_desc(virtq, desc1);
	virtq_free_desc(virtq, desc2);
	virtq_free_desc(virtq, desc3);
	slab_free(req);

	return;
bad_desc:
	puts("virtio-blk received malformed descriptors\n");
	return;

bad_status:
	puts("virtio-blk: error in command response\n");
	return;
}
```

This is a deceptively long function, all of the complexity exists mainly in
checking whether we receive the same number of descriptors we sent (3) and
ensuring that the descriptors are the same size. There's no reason why this
wouldn't be the case, since the device should return the same descriptor chain
which we sent to it. However, it's important to check these cases anyway. Once
we've done all of that checking, we extract `req`, the original block request,
and `data`, the buffer for read/write. We check the status, and if it isn't OK,
we print an error message. Finally, if this was a read request (IN), we simply
print out the block as if it were a string. Obviously, this is bad general
purpose behavior, but this driver is really just trying to get to
proof-of-concept here.

Once we've "handled" the response, we mark each descriptor as free to be used
for another request, and we free the block request as well.

### Putting it all together

To demonstrate all this functionality, I created kernel shell commands for both
read and write. Here is an example of all of this in action!

```
$ make run
Running. Exit with Ctrl-A X

qemu-system-arm -M virt -global virtio-mmio.force-legacy=false -drive file=mydisk,if=none,format=raw,id=hd -device virtio-blk-device,drive=hd -kernel kernel.bin -nographic
SOS: Startup
... lots of virtio-blk debugging output I need to clean up ...
Stephen's OS (user shell, pid=2)
ush> exit
[kernel] Process 2 exited with code 0.
[kernel] WARNING: no more processes remain
Stephen's OS, v0.1
ksh> blkwrite 1 this_is_a_test
ksh> blkread 1
virtio-blk: result: "this_is_a_test"
ksh> blkwrite 1 this_is_a_second_test
ksh> blkread 1
ksh> virtio-blk: result: "this_is_a_second_test"
```

Since the functionality can only be accessed by the kernel, I had to kill my
userspace shell process, which starts up the kernel shell (note the `ksh>`)
prompt.

The example shows me writing a simple string to sector 1 (the second sector) of
a hard drive, and then reading it back, and changing it. If you exit and restart
the VM, you can see that the reads and writes persist across reboots too!

### Closing notes

This has been a really long article, which I think accurately depicts the
complexity of working on a component of an OS. In this article, we've only
implemented the barest minimum amount to qualify being a "block driver", yet
there was a lot of complexity involved, ranging from alignment, memory barriers,
virtqueues, interrupts, and a couple standards documents (Device Tree and Virtio
being the most relevant). But the complexity feels manageable. Once something
works, you can extend it, improve it, and enhance it. There are lots of
enhancements I intend to make for this system:

1. The block device should offer an API to return the read data to a calling
   function (outside of the interrupt context). Currently we just print it out!
2. There are several extension features to the virtio block device specification
   which allow more efficient use. Most block devices don't operate in block
   sizes of 512 bytes, typically much larger. These extra features allow us to
   learn the correct block sizes so we can tune our accesses. We should use
   these features!
3. We should implement a file system to go on top of the block device.

But for the meantime, I'm just proud to have a working block device inside of my
operating system.

If you've found this interesting, you can browse the full code as it was at the
time of this writing by these links: [virtio.c][virtio-c] and
[virtio.h][virtio-h]. Thanks for spending the time to read this article, and if
you have any feedback, please feel free to share it with me via email or social
media (see the homepage for links).

[sos-preempt]: {% post_url 2020-02-08-sos-preemptive-multitasking %}
[sos-gh]: https://github.com/brenns10/sos
[virtio]: http://docs.oasis-open.org/virtio/virtio/v1.0/cs04/virtio-v1.0-cs04.html
[lwn-virtio-without-virt]: https://lwn.net/Articles/805235/
[dtree]: https://www.devicetree.org/
[so]: https://stackoverflow.com/questions/52037482/qemu-virtio-blk-strange-restrictions
[virtio-c]: https://github.com/brenns10/sos/blob/13a2d89cb8edbb45535279d2a4f07ed74c53ec91/kernel/virtio.c
[virtio-h]: https://github.com/brenns10/sos/blob/13a2d89cb8edbb45535279d2a4f07ed74c53ec91/kernel/virtio.h
