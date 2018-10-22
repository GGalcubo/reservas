/*HELPER*/

/**
 * Muestra ventana de notificación
 * @param msg
 * @param state = 'error','success','info'
 */
showMsg = (msg, state = 'error') => {    
    toastr[state](msg);
};