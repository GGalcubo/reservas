/*HELPER*/

/* msg = string
   state = ('error','info','success')
 */
showMsg = (msg, state = 'error') => {    
    toastr[state](msg);
};