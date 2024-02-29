#include <linux/module.h> /* for all kernel modules */
#include <linux/kernel.h> /* for KERN_INFO */
int init_module( void ){
    printk( KERN_INFO "Hello Jiankun's OS! \n" );
    return 0;
}

void cleanup_module( void ){
    printk( KERN_INFO "Goodbye, Jianun's OS! \n" );
    return;
}


MODULE_LICENSE("GPL");
MODULE_DESCRIPTION("Homework3 Kernel Module");
MODULE_AUTHOR("JiankunDong");
