$(document).ready( () => {

    $('#fecha').datepicker({
        language: 'es',
        dateFormat: 'dd/mm/yy',
        // todayBtn: true,
        todayHighlight: true,
        autoclose: true,
        beforeShow: () => {
            setTimeout( () => {
                $('.ui-datepicker').css('z-index', 99999999999999);
            }, 0);
        }
    });

    console.log('permiso: ' + permiso);

    //$('#admin_total').val(0);

    $('#admin_espera_cliente, #admin_estacionamiento_cliente, #admin_estacionamiento_cliente, #admin_peaje_cliente, #admin_hs_dispo_cliente, #admin_costo_cliente, #admin_costo_bilingue_cliente, #admin_costo_maletas_cliente, #admin_otros_cliente').on('input', function () {
        let sum_total = 0;
        sum_total += parseInt($('#admin_espera_cliente').val()) || 0;
        sum_total += parseInt($('#admin_estacionamiento_cliente').val()) || 0;
        sum_total += parseInt($('#admin_peaje_cliente').val()) || 0;
        sum_total += parseInt($('#admin_hs_dispo_cliente').val()) || 0;
        sum_total += parseInt($('#admin_costo_cliente').val()) || 0;
        sum_total += parseInt($('#admin_costo_bilingue_cliente').val()) || 0;
        sum_total += parseInt($('#admin_costo_maletas_cliente').val()) || 0;
        sum_total += parseInt($('#admin_otros_cliente').val()) || 0;

        $('#admin_total_cliente').val(sum_total);
    });

    $('#admin_espera_proveedor, #admin_estacionamiento_proveedor, #admin_estacionamiento_proveedor, #admin_peaje_proveedor, #admin_hs_dispo_proveedor, #admin_costo_proveedor, #admin_costo_bilingue_proveedor, #admin_costo_maletas_proveedor, #admin_otros_proveedor').on('input', function () {
        let sum_total = 0;
        sum_total += parseInt($('#admin_espera_proveedor').val()) || 0;
        sum_total += parseInt($('#admin_estacionamiento_proveedor').val()) || 0;
        sum_total += parseInt($('#admin_peaje_proveedor').val()) || 0;
        sum_total += parseInt($('#admin_hs_dispo_proveedor').val()) || 0;
        sum_total += parseInt($('#admin_costo_proveedor').val()) || 0;
        sum_total += parseInt($('#admin_costo_bilingue_proveedor').val()) || 0;
        sum_total += parseInt($('#admin_costo_maletas_proveedor').val()) || 0;
        sum_total += parseInt($('#admin_otros_proveedor').val()) || 0;

        $('#admin_total_proveedor').val(sum_total);
    });

    $(".cont_desde_provincia").hide();
    $(".cont_hasta_provincia").hide();
    $(".cont_modal_desde_provincia").hide();
    $(".cont_modal_hasta_provincia").hide();
    $(".hasta_vuelo").hide();
    $(".desde_vuelo").hide();
    $(".modal_desde_vuelo").hide();
    $(".modal_hasta_vuelo").hide();
    //$("#administracion").hide();
    $("#administracion_tab_btn a").hide();

    if(es_nuevo == '1'){
        //$('#fecha').datepicker('setDate', 'blank');
        //$("#viaje-tab").hide();
        $("#viaje-tab").show();
        $("#hora").val('') ;
        $("#hora_estimada").val('');
        $('#estado').attr("disabled", true);
        $('#clonar_btn').hide();
    }else{
        if(is_clone == '1'){
            $("#hora").val('') ;
            $("#hora_estimada").val('');
        }
        $("#viaje-tab").show();
        getGrillasHistorial();
        if(estado == '7'){
            //$("#administracion").show();
            if(permiso != 'operaciones' or permiso != 'unidades'){
                $("#administracion_tab_btn a").show();
            }

        }
        if(mensaje != ''){showMsg(mensaje, 'success')}
        $('#viaje_titulo').html('Ingreso del Cliente y Datos del Viaje ' + viaje);
    }
    getClientes(es_nuevo);
    if(bilingue_viaje === 'True'){
        $('#bilingue').prop('checked', true);
    }
    $('#maletas').val(maletas_viaje);
    $('#tiempo_espera').val(espera_viaje);
    $('#tiempo_hs_dispo').val(dispo_viaje);
    $('#pasajero_cant').val(pasajero_cant);

    $('#categoria_viaje').select2({ placeholder: 'Seleccionar', width: 'auto'});
    $('#contacto').select2({ placeholder: 'Seleccionar', width: 'auto'});
    $("#pasajero").on("select2:select", function (e) { updateFillsByPasajero("select2:select", e); });
    $('#pasajero').select2({ placeholder: 'Seleccionar', width: 'auto'});
    $('#pasajero_trayecto').select2({ placeholder: 'Seleccionar Pasajero', width: 'auto', dropdownParent: $('#add_tramo')});

    $("#id_cliente").on("select2:select", function (e) { updateFillsByCliente("select2:select", e); });
    $('#id_cliente').select2({ placeholder: 'Seleccionar Cliente', width: 'auto'});
    //$("#unidad_id").on("select2:select", function (e) { updateFillsByUnidad("select2:select", e); });
    $('#unidad_id').select2({placeholder: 'Seleccionar', width: 'auto'});
    $('#centroDeCosto').select2({placeholder: 'Seleccionar', width: 'auto'});


    $("#desde_destino").on("select2:select", function (e) { updateFillsByDestino("select2:select", e); });
    $('#desde_destino').select2({placeholder: 'Seleccionar', width: 'auto'});
    $("#hasta_destino").on("select2:select", function (e) { updateFillsByDestino("select2:select", e); });
    $('#hasta_destino').select2({placeholder: 'Seleccionar', width: 'auto'});
    $("#modal_desde_destino").on("select2:select", function (e) { updateFillsByDestino("select2:select", e); });
    $('#modal_desde_destino').select2({placeholder: 'Seleccionar', dropdownParent: $('#add_tramo')});
    $("#modal_hasta_destino").on("select2:select", function (e) { updateFillsByDestino("select2:select", e); });
    $('#modal_hasta_destino').select2({placeholder: 'Seleccionar', dropdownParent: $('#add_tramo')});
    $('#modal_hasta_provincia').select2({placeholder: 'Seleccionar', dropdownParent: $('#add_tramo')});

    $("#desde_localidad").on("select2:select", function (e) { updateFillsByLocalidad("select2:select", e); });
    $('#desde_localidad').select2({placeholder: 'Seleccionar', width: 'auto'});
    $("#hasta_localidad").on("select2:select", function (e) { updateFillsByLocalidad("select2:select", e); });
    $('#hasta_localidad').select2({placeholder: 'Seleccionar', width: 'auto'});
    $("#modal_desde_localidad").on("select2:select", function (e) { updateFillsByLocalidad("select2:select", e); });
    $('#modal_desde_localidad').select2({placeholder: 'Seleccionar', dropdownParent: $('#add_tramo')});
    $("#modal_hasta_localidad").on("select2:select", function (e) { updateFillsByLocalidad("select2:select", e); });
    $('#modal_hasta_localidad').select2({placeholder: 'Seleccionar', dropdownParent: $('#add_tramo')});
    $('#modal_desde_provincia').select2({placeholder: 'Seleccionar', dropdownParent: $('#add_tramo')});

    var tmp_tipo_observacion;
    $('#tipo_viaje_obs').append($('<option>').text('').attr('value', ''));
    $.each(tipo_observaciones, (i, value) => {
        if(tmp_tipo_observacion != value.tipo_observacion){
            $('#tipo_viaje_obs').append($('<option>').text(value.tipo_observacion).attr('value', value.tipo_observacion));
        }
        tmp_tipo_observacion = value.tipo_observacion;
    });

    $('#tipo_viaje_obs').on('change', e => {
        var valueSelected = $('#tipo_viaje_obs').val();
        $('#detalle_obs').empty();

        $.each(tipo_observaciones, (i, value) => {
            if(valueSelected == value.tipo_observacion){
              $('#detalle_obs').append($('<option>').text(value.detalle_tipo_obs).attr('value', value.id));
            }
        });
    });

    $('.guardar_viaje').click(function() {
        guardarViaje();
    });

    $("#form-viaje-viaje").submit( e => {
        guardarViaje();
        e.preventDefault(); // avoid to execute the actual submit of the form.
    });


    $(document).on( "click", '.delete_button', function(){
        var obj               = {};
        obj.id                = $(this).data('id');
        obj.idViaje           = viaje;
        var url = "/sistema/borrarTrayecto/";
        $.ajax({
               type: "POST",
               url: url,
               headers: {'X-CSRFToken': csrf_token},
               data: obj,
               success: data => {
                   if(data.error == '1'){
                      showMsg(data.msg, 'error');
                   }else{
                      $("#grillaTramos").html(data);
                   }
               }
             });
    });

    $(document).on( "click", '#add_button', e => {
        $("#modal_id").val('0');

        $("#modal_desde_destino").val('').trigger('change');
        $("#modal_desde_provincia").val('').trigger('change');
        $("#modal_desde_localidad").val('').trigger('change');
        $("#modal_hasta_destino").val('').trigger('change');
        $("#modal_hasta_provincia").val('').trigger('change');
        $("#modal_hasta_localidad").val('').trigger('change');

        $("#modal_desde_calle").val('');
        $("#modal_desde_altura").val('');
        $("#modal_desde_entre").val('');
        $("#modal_desde_vuelo").val('');
        $("#modal_desde_compania").val('');
        $("#modal_hasta_calle").val('');
        $("#modal_hasta_altura").val('');
        $("#modal_hasta_entre").val('');
        $("#modal_hasta_vuelo").val('');
        $("#modal_hasta_compania").val('');
        $("#pasajero_trayecto").val('').trigger('change');

        $(".cont_modal_hasta_localidad").show();
        $(".cont_modal_desde_localidad").show();
        $(".modal_hasta_direccion").show();
        $(".modal_desde_direccion").show();
        $(".cont_modal_desde_provincia").hide();
        $(".cont_modal_hasta_provincia").hide();
        $(".modal_desde_vuelo").hide();
        $(".modal_hasta_vuelo").hide();
    });


    $('.edit_button').click(function() {

        let id                  = $(this).data('id');

        let provincia_desde     = $(this).data('provincia_desde');
        let localidad_desde     = $(this).data('localidad_desde');
        let destino_desde       = $(this).data('provincia_desde');
        let provincia_hasta     = $(this).data('provincia_hasta');
        let localidad_hasta     = $(this).data('localidad_hasta');
        let destino_hasta       = $(this).data('provincia_hasta');

        let calle_desde         = $(this).data('calle_desde');
        let altura_desde        = $(this).data('altura_desde');
        let entre_desde         = $(this).data('entre_desde');
        let compania_desde      = $(this).data('compania_desde');
        let vuelo_desde         = $(this).data('vuelo_desde');
        let calle_hasta         = $(this).data('calle_hasta');
        let altura_hasta        = $(this).data('altura_hasta');
        let entre_hasta         = $(this).data('entre_hasta');
        let compania_hasta      = $(this).data('compania_hasta');
        let vuelo_hasta         = $(this).data('vuelo_hasta');
        let pasajero_trayecto   = $(this).data('pasajero_trayecto');

        $("#modal_id").val(id);

        $("#modal_desde_destino").val(provincia_desde).trigger('change');
        $("#modal_desde_localidad").val(localidad_desde).trigger('change');
        //$("#modal_desde_provincia").val(provincia_desde).trigger('change');
        $("#modal_hasta_destino").val(provincia_hasta).trigger('change');
        $("#modal_hasta_localidad").val(localidad_hasta).trigger('change');
        //$("#modal_hasta_provincia").val(provincia_hasta).trigger('change');

        $("#modal_desde_calle").val(calle_desde);
        $("#modal_desde_altura").val(altura_desde);
        $("#modal_desde_entre").val(entre_desde);
        $("#modal_desde_compania").val(compania_desde);
        $("#modal_desde_vuelo").val(vuelo_desde);
        $("#modal_hasta_calle").val(calle_hasta);
        $("#modal_hasta_altura").val(altura_hasta);
        $("#modal_hasta_entre").val(entre_hasta);
        $("#modal_hasta_compania").val(compania_hasta);
        $("#modal_hasta_vuelo").val(vuelo_hasta);
        $("#pasajero_trayecto").val(pasajero_trayecto).trigger('change');

        let evt = {};
        evt.params = {};
        evt.params.data = {};

        evt.params.data.id = provincia_desde;
        evt.params.data.provincia_select_id = provincia_desde;
        evt.params.data.localidad_select_id = localidad_desde;
        evt.params.data.init = true;
        evt.currentTarget = {};
        evt.currentTarget.id = 'modal_desde_destino';
        updateFillsByDestino('', evt);

        evt.currentTarget.id = 'modal_desde_localidad';
        evt.params.data.id = localidad_desde;
        updateFillsByLocalidad('', evt);

        evt.params.data.id = provincia_hasta;
        evt.params.data.provincia_select_id = provincia_hasta;
        evt.params.data.localidad_select_id = localidad_hasta;
        evt.params.data.init = true;
        evt.currentTarget = {};
        evt.currentTarget.id = 'modal_hasta_destino';
        updateFillsByDestino('', evt);

        evt.params.data.id = localidad_hasta_id;
        evt.currentTarget.id = 'modal_hasta_localidad';
        updateFillsByLocalidad('', evt);

        /*if(provincia_desde != ''){
            $(".cont_modal_desde_localidad").hide();
            $(".modal_desde_direccion").show();
            $(".cont_modal_desde_provincia").show();
            $(".modal_desde_vuelo").hide();
        }else{
            $(".cont_modal_desde_localidad").show();
            $(".modal_desde_direccion").show();
            $(".cont_modal_desde_provincia").hide();
            $(".modal_desde_vuelo").hide();
        }*/

        /*if(provincia_hasta != ''){
            $(".cont_modal_hasta_localidad").hide();
            $(".modal_hasta_direccion").show();
            $(".cont_modal_hasta_provincia").show();
            $(".modal_hasta_vuelo").hide();
        }else{
            $(".cont_modal_hasta_localidad").show();
            $(".modal_hasta_direccion").show();
            $(".cont_modal_hasta_provincia").hide();
            $(".modal_hasta_vuelo").hide();
        }*/
        /*if(localidad_desde == 9){
            $(".cont_modal_desde_localidad").show();
            $(".modal_desde_vuelo").show();
        }
        if(localidad_hasta == 9){
            $(".cont_modal_hasta_localidad").show();
            $(".modal_hasta_vuelo").show();
        }*/

        var terminal_flag_desde;
        var terminal_flag_hasta;
        $.each(localidades, function(i, value) {
            if(value.id == localidad_desde){
                terminal_flag_desde = value.terminal_flag;
            }
        });

        if(terminal_flag_desde == 'True'){
            $(".modal_desde_direccion").hide();
            $(".modal_desde_vuelo").show();
        }else{
            $(".modal_desde_direccion").show();
            $(".modal_desde_vuelo").hide();
        }
        $.each(localidades, function(i, value) {
            if(value.id == localidad_hasta){
                terminal_flag_hasta = value.terminal_flag;
            }
        });

        if(terminal_flag_hasta == 'True'){
            $(".modal_hasta_direccion").hide();
            $(".modal_hasta_vuelo").show();
        }else{
            $(".modal_hasta_direccion").show();
            $(".modal_hasta_vuelo").hide();
        }

        //$(".modal-title").text('Editar Tramo');
    });

    //$( "#pasajero" ).change(updateFillsByPasajero);

    $("#guardarAdjunto").submit( evt => {
       evt.preventDefault();
       var formData = new FormData(document.getElementById("guardarAdjunto"));
       formData.append("idViaje", viaje);
       $.ajax({
            url: '/sistema/guardarViajeAdjunto/',
            type: 'POST',
            headers: {'X-CSRFToken': csrf_token},
            data: formData,
            async: false,
            cache: false,
            contentType: false,
            enctype: 'multipart/form-data',
            processData: false,
            success: data => {
                $('#grillaAdjuntos').html(data);
            }
       });
       return false;
     });

    $('#tablaTramos').DataTable({
        responsive: true,
        // scrollY: 200,
        order: [[ 0, "asc" ]],
        lengthMenu: [
                        [ -1, 500, 100, 50, 25, 10 ],
                        [ 'Todos', '500', '100', '50', '25', '10' ]
                    ],
        language: {
            url: '//cdn.datatables.net/plug-ins/1.10.15/i18n/Spanish.json'
        }
    });

    $('#tablaObservacionViajes').DataTable({
        responsive: true,
        // scrollY: 200,
        order: [[ 0, "asc" ]],
        lengthMenu: [
                        [ -1, 500, 100, 50, 25, 10 ],
                        [ 'Todos', '500', '100', '50', '25', '10' ]
                    ],
        language: {
            url: '//cdn.datatables.net/plug-ins/1.10.15/i18n/Spanish.json'
        }
    });

    $('#hora').timepicker();
    $('#hora_estimada').timepicker();
    $('#hora_obs').timepicker();

    $('#tablaPasajeroClientes').DataTable({
        responsive: true,
        // scrollY: 200,
        order: [[ 1, "asc" ]],
        lengthMenu: [
                        [ -1, 500, 100, 50, 25, 10 ],
                        [ 'Todos', '500', '100', '50', '25', '10' ]
                    ],
        language: {
            url: '//cdn.datatables.net/plug-ins/1.10.15/i18n/Spanish.json'
        },
    });

    $('#tablaPasajeroViaje').DataTable({
        responsive: true,
        // scrollY: 200,
        order: [[ 1, "asc" ]],
        lengthMenu: [
                        [ -1, 500, 100, 50, 25, 10 ],
                        [ 'Todos', '500', '100', '50', '25', '10' ]
                    ],
        language: {
            url: '//cdn.datatables.net/plug-ins/1.10.15/i18n/Spanish.json'
        },
    });

    $('#tablaHistorialViaje').DataTable({
        responsive: true,
        // scrollY: 200,
        order: [[ 0, "asc" ]],
        lengthMenu: [
                        [ -1, 500, 100, 50, 25, 10 ],
                        [ 'Todos', '500', '100', '50', '25', '10' ]
                    ],
        language: {
            url: '//cdn.datatables.net/plug-ins/1.10.15/i18n/Spanish.json'
        },
    });

});

guardarViaje = () =>{
    if ($("#id_cliente").val() == ""){
            showMsg("El campo cliente es obligatorio.");
            return false;
        }
        if ($("#centroDeCosto").val() == ""){
            showMsg("El campo centro de costo es obligatorio.");
            return false;
        }
        if ($("#contacto").val() == ""){
            showMsg("El campo solicitante es obligatorio.");
            return false;
        }
        if ($("#pasajero").val() == ""){
            showMsg("El campo pasajero es obligatorio.");
            return false;
        }
        if ($("#fecha").val() == "//"){
            showMsg("El campo fecha es obligatorio.");
            return false;
        }
        if ($("#hora").val() == ""){
            showMsg("El campo hora es obligatorio.");
            return false;
        }
        /*if ($("#hora_estimada").val() == ""){
            showMsg("El campo hora estimada es obligatorio.");
            return false;
        }*/
        if ($("#categoria_viaje").val() == ""){
            showMsg("El campo categoria viaje es obligatorio.");
            return false;
        }
        if($("#estado").val() == '6' || $("#estado").val() == '7'){
            if ($("#unidad_id").val() == ""){
                showMsg("El campo unidad es obligatorio.");
                return false;
            }
        }
        if(es_nuevo != '1'){

        }
        if ($("#estado").val() == ""){
            showMsg("El campo estado es obligatorio.");
            return false;
        }
        if ($("#tiempo_espera").val() != "" && $("#tiempo_espera").val() < 15){
            showMsg("La espera minima es 15 min.");
            return false;
        }
        if ($("#tiempo_hs_dispo").val() != "" && $("#tiempo_hs_dispo").val() < 1){
            showMsg("El horario disponible minimo es 1 hs.");
            return false;
        }

        var obj               = {};
        obj.estado            = $("#estado").val();
        obj.cliente           = $("#id_cliente").val();
        obj.contacto          = $("#contacto").val();
        obj.centro_costos     = $("#centroDeCosto").val();
        obj.pasajero          = $("#pasajero").val();
        obj.fecha             = $("#fecha").val();
        obj.hora              = ($("#hora").val().length == 5) ? $("#hora").val() : '0' + $("#hora").val();
        obj.hora_estimada     = ($("#hora_estimada").val().length == 5) ? $("#hora_estimada").val() : '0' + $("#hora_estimada").val();
        obj.costo_proveedor   = $("#costo_proveedor").val();
        obj.tarifa_pasada     = $("#tarifa_pasada").val();
        obj.comentario_chofer = $("#comentario_chofer").val();
        obj.unidad            = $("#unidad_id").val();
        obj.espera            = $("#espera").val();
        obj.tiempo_espera     = $("#tiempo_espera").val();
        obj.peaje             = $("#peaje").val();
        obj.otros             = $("#otros").val();
        obj.estacionamiento   = $("#estacionamiento").val();
        obj.categoria_viaje   = $("#categoria_viaje").val();
        obj.maletas           = $("#maletas").val();
        obj.costo_maletas     = $("#costo_maletas").val();
        obj.bilingue          = $("#bilingue:checked").val() || '';
        obj.costo_bilingue    = $("#costo_bilingue").val();
        obj.cod_externo       = $("#cod_externo").val();
        obj.nro_aux           = $("#nro_aux").val();
        obj.tipo_pago         = $("#tipo_pago").val();
        obj.importe_efectivo  = $("#importe_efectivo").val();
        obj.tiempo_hs_dispo   = $("#tiempo_hs_dispo").val();
        obj.hs_dispo          = $("#hs_dispo").val();
        obj.pasajero_cant     = $("#pasajero_cant").val();
        obj.es_nuevo          = es_nuevo;

        //TRAYECTO PRINCIPAL
        obj.desde_destino     = $("#desde_destino").val();
        obj.desde_localidad   = $("#desde_localidad").val();
        obj.desde_provincia   = $("#desde_provincia").val();
        obj.desde_calle       = $("#desde_calle").val();
        obj.desde_altura      = $("#desde_altura").val();
        obj.desde_entre       = $("#desde_entre").val();
        obj.desde_compania    = $("#desde_compania").val();
        obj.desde_vuelo       = $("#desde_vuelo").val();
        obj.hasta_destino     = $("#hasta_destino").val();
        obj.hasta_localidad   = $("#hasta_localidad").val();
        obj.hasta_provincia   = $("#hasta_provincia").val();
        obj.hasta_altura      = $("#hasta_altura").val();
        obj.hasta_calle       = $("#hasta_calle").val();
        obj.hasta_entre       = $("#hasta_entre").val();
        obj.hasta_compania    = $("#hasta_compania").val();
        obj.hasta_vuelo       = $("#hasta_vuelo").val();
        obj.principal         = 1;
        //

        if(es_nuevo == 0){
            obj.idViaje = viaje;
        }else{
            obj.mensaje = 1;
        }

        var url = "/sistema/guardarViaje/";
        $.ajax({
           type: "POST",
           url: url,
           headers: {'X-CSRFToken': csrf_token},
           data: obj,
           success: data => {
                if(data.error === '1'){
                    showMsg(data.msg, 'error');
                }else{
                    /*data.url ? window.location.replace(data.url) : */showMsg('Los datos se han actualizado correctamente.', 'success');
                    if(es_nuevo == '1'){
                        es_nuevo = 0;
                        viaje = data.viaje;
                        idViaje = data.viaje;
                        $("#idViajeObser").val(idViaje);
                        $('#viaje_titulo').html('Ingreso del Cliente y Datos del Viaje ' + viaje);
                        $('#clonar_btn').show();
                    }

                    if(obj.estado == 7){
                        if(data.error != 0){
                            viaje_items = [];
                            $.each(data, (k, item) => {
                                let obj = {
                                    id : item.pk,
                                    monto : item.fields.monto,
                                    monto_s_iva : item.fields.monto_s_iva,
                                    monto_iva : item.fields.monto_iva,
                                    tipo_items_viaje : item.fields.tipo_items_viaje.toString(),
                                    cant: item.fields.cant};
                                viaje_items.push(obj);
                            });
                            fillViajeItems();
                            //$("#administracion").show();
                            if(permiso != 'operaciones'){
                                $("#administracion_tab_btn a").show();
                            }
                        }
                    }else{
                        //$("#administracion").hide();
                        $("#administracion_tab_btn a").hide();
                    }
                }
                getGrillasHistorial();
           }
        });
};

guardarViajeTrayecto = () =>{
    var obj               = {};
    obj.desde_destino     = $("#desde_destino").val();
    obj.desde_localidad   = $("#desde_localidad").val();
    obj.desde_provincia   = $("#desde_provincia").val();
    obj.desde_calle       = $("#desde_calle").val();
    obj.desde_altura      = $("#desde_altura").val();
    obj.desde_entre       = $("#desde_entre").val();
    obj.desde_compania    = $("#desde_compania").val();
    obj.desde_vuelo       = $("#desde_vuelo").val();
    obj.hasta_destino     = $("#hasta_destino").val();
    obj.hasta_localidad   = $("#hasta_localidad").val();
    obj.hasta_provincia   = $("#hasta_provincia").val();
    obj.hasta_altura      = $("#hasta_altura").val();
    obj.hasta_calle       = $("#hasta_calle").val();
    obj.hasta_entre       = $("#hasta_entre").val();
    obj.hasta_compania    = $("#hasta_compania").val();
    obj.hasta_vuelo       = $("#hasta_vuelo").val();
    obj.pasajero          = $("#pasajero").val();
    obj.principal         = 1;
    obj.idViaje           = viaje;


    var url = "/sistema/guardarTrayecto/";
    $.ajax({
           type: "POST",
           url: url,
           headers: {'X-CSRFToken': csrf_token},
           data: obj,
           success: data => {
              showMsg(data.msg, 'success');
           }
         });

    e.preventDefault();
};

/**
 *
 */
getClientes = es_nuevo => {
    let url = "/sistema/getClientes/";
    $.ajax({
        type: "POST",
        url: url,
        headers: {'X-CSRFToken': csrf_token},
        data: {},
        success: function(data)
        {
            $.each(data, (k, item) => {
                let obj = {
                    id : item.pk,
                    razon_social : item.fields.razon_social
                };
                clientes.push(obj);
                if(item.pk === cliente_id){
                    $('#id_cliente').append($('<option selected="selected">').text(item.pk + ' - ' + item.fields.razon_social).attr('value', item.pk));
                }else{
                    $('#id_cliente').append($('<option>').text(item.pk + ' - ' + item.fields.razon_social).attr('value', item.pk));
                }
            });

            //HAGO ESTO PARA SIMULAR UN EVENTO QUE PIDE LA FUNCION DE SELECT2ME

            let evt = {};
            evt.params = {};
            evt.params.data = {};
            evt.params.data.no_borrar_pasajeros = true;

            if(es_nuevo != '1') {
                evt.params.data.id = cliente_id;
                updateFillsByCliente('', evt);
            }

            getDetinos(evt);

        }
    });
};

getDetinos = evt => {
    evt.params.data.id = provincia_desde_id;
    evt.params.data.provincia_select_id = provincia_desde_id;
    evt.params.data.localidad_select_id = localidad_desde_id;
    evt.params.data.init = true;
    evt.currentTarget = {};
    evt.currentTarget.id = 'desde_destino';
    updateFillsByDestino('', evt);

    evt.currentTarget.id = 'desde_localidad';
    evt.params.data.id = localidad_desde_id;
    updateFillsByLocalidad('', evt);

    evt.params.data.id = provincia_hasta_id;
    evt.params.data.provincia_select_id = provincia_hasta_id;
    evt.params.data.localidad_select_id = localidad_hasta_id;
    evt.params.data.init = true;
    evt.currentTarget = {};
    evt.currentTarget.id = 'hasta_destino';
    updateFillsByDestino('', evt);

    evt.params.data.id = localidad_hasta_id;
    evt.currentTarget.id = 'hasta_localidad';
    updateFillsByLocalidad('', evt);

    fillViajeItems();
};

/**
 *
 */
getGrillasHistorial = () => {
    let url = "/sistema/getHistorial/";
    $.ajax({
        type: "POST",
        url: url,
        headers: {'X-CSRFToken': csrf_token},
        data: {idViaje},
        success: function(data)
        {
            $('#cont_table_historial').empty().html(data);
        }
    });
};

/**
 * Cris, te dejo esto del html cliente, que es de donde saqué el modal ya armado
 * @returns {boolean}
 */
guardarSolicitante = () => {
    if ($('#nombrePasajeroCliente').val() == ""){
        showMsg("El Nombre es obligatorio.")
        return false;
    }
    if ($('#apellidoPasajeroCliente').val() == ""){
        showMsg("El Apellido es obligatorio.")
        return false;
    }
    var url = "/sistema/guardarSolicitanteDesdeViaje/";
    $.ajax({
        type: "POST",
        url: url,
        headers: {'X-CSRFToken': csrf_token},
        data: $("#form-datos-cliente-solicitante").serialize(),
        success: data => {
            $('#idSolicitante').val("0");
            $('#nombrePasajeroCliente').val("");
            $('#apellidoPasajeroCliente').val("");
            $('#puestoSol').val("");
            $('#mailSol').val("");
            $('#telefonoSol').val("");
            $('#contacto').html(data);
            $('#add_solicitante').modal('toggle');
        }
    });
};

/**
 *
 * @returns {boolean}
 */
clonarViaje = () => {
    var url = "/sistema/clonarViaje/";
    $.ajax({
        type: "POST",
        url: url,
        headers: {'X-CSRFToken': csrf_token},
        data: {'idViaje':idViaje},
        success: data => {
            window.open('/sistema/editaViaje/?idViaje=' + data.viaje_a_clonar + '&c=1', '_blank');
        }
    });
};
/**
 *
 */
recalcularViajeAdmin = () =>{
    let url = "/sistema/guardaViajeAdmin/";
    $.ajax({
        type: "POST",
        url: url,
        headers: {'X-CSRFToken': csrf_token},
        data: $("#form-guarda-viaje-admin").serialize()+'&'+$.param({ 'tiempo_hs_dispo': $('#tiempo_hs_dispo').val(),
                                                                     'tiempo_espera': $('#tiempo_espera').val(),
                                                                     'bilingue': $("#bilingue:checked").val() || '',
                                                                     'maletas': $("#maletas").val(),
                                                                     'metodo':'recalcular'
                                                                    }),
        success: data => {
            showMsg('Se guardo con exito', 'success');
            viaje_items = [];
            $.each(data, (k, item) => {
                let obj = {
                    id : item.pk,
                    monto : item.fields.monto,
                    monto_s_iva : item.fields.monto_s_iva,
                    monto_iva : item.fields.monto_iva,
                    tipo_items_viaje : item.fields.tipo_items_viaje.toString() ,
                    cant: item.fields.cant};
                viaje_items.push(obj);
            });
            fillViajeItems();
        }
    });
};

/**
 *
 */
guardaViajeAdmin = () => {
    let url = "/sistema/guardaViajeAdmin/";
    $.ajax({
        type: "POST",
        url: url,
        headers: {'X-CSRFToken': csrf_token},
        data: $("#form-guarda-viaje-admin").serialize()+'&'+$.param({ 'tiempo_hs_dispo': $('#tiempo_hs_dispo').val(),
                                                                     'tiempo_espera': $('#tiempo_espera').val(),
                                                                     'bilingue': $("#bilingue:checked").val() || '',
                                                                     'maletas': $("#maletas").val(),
                                                                     'metodo':'guarda'
                                                                    }),
        success: data => {
            showMsg('Se guardo con exito', 'success');
            viaje_items = [];
            $.each(data, (k, item) => {
                let obj = {
                    id : item.pk,
                    monto : item.fields.monto,
                    monto_s_iva : item.fields.monto_s_iva,
                    monto_iva : item.fields.monto_iva,
                    tipo_items_viaje : item.fields.tipo_items_viaje.toString() ,
                    cant: item.fields.cant};
                viaje_items.push(obj);
            });
            fillViajeItems();
        }
    });
};

/**
 *
 */
sumarPasajero = () => {
    let url = "/sistema/guardaViajePasajeroPOST/";
    $.ajax({
        type: "POST",
        url: url,
        headers: {'X-CSRFToken': csrf_token},
        data: {pasajero:$('#suma_pasajero').val(), viaje},
        success: data => {
            showMsg('Agregado con exito', 'success');
            $('#grillaPasajero').html(data);
        }
    });
};

/**
 *
 */
getViajePasajeros = () => {
    let url       = "/sistema/getViajePasajeros/";
    let pasajeros = {};
    $.ajax({
        type: "POST",
        url: url,
        headers: {'X-CSRFToken': csrf_token},
        data: {viaje},
        success: data => {
            //console.table(data);
            pasajeros = data;
        }
    });
    return pasajeros;
};

/**
 *
 */
updateFillsByPasajero = (name, evt) =>{
    $('#suma_pasajero').empty();
    let pasajeros = getViajePasajeros;
    $.each(cliente.personascliente, (i, persona) => {
        if(persona.tipo_persona == 'Pasajero'){
            if(persona.id != $('#pasajero').val()){
                let ya_fue_agregado = false;
                $.each(pasajeros, (k, pasajero) => {
                    if(pasajero.pk === persona.id){
                        ya_fue_agregado = true;
                    }
                });
                if(!ya_fue_agregado){
                    $('#suma_pasajero').append($('<option>').text(persona.nombre).attr('value', persona.id));
                }
            }
        }
    });

    let url = "/sistema/getTelefonoPasajeroById/";
    $.ajax({
        type: "POST",
        url: url,
        headers: {'X-CSRFToken': csrf_token},
        data: {cliente_id: $('#id_cliente').val(), pasajero_id: evt.params.data.id},
        success: function (data) {
            $('#pasajero_telefono').val(data.telefono);
        }
    });
};

/**
 *
 * @param adjunto_id
 */
deleteViajeAdjunto = adjunto_id =>{
    let url       = "/sistema/deleteViajeAdjunto/";
    $.ajax({
        type: "POST",
        url: url,
        headers: {'X-CSRFToken': csrf_token},
        data: {adjunto_id,viaje},
        success: data => {
            //console.table(data);
            $('#grillaAdjuntos').html(data);
        }
    });
};

/**
 *
 * @param pasajero_id
 */
deleteViajePasajero = pasajero_id =>{
    let url       = "/sistema/deleteViajePasajero/";
    $.ajax({
        type: "POST",
        url: url,
        headers: {'X-CSRFToken': csrf_token},
        data: {pasajero:pasajero_id,viaje},
        success: data => {
            //console.table(data);
            $('#grillaPasajero').html(data);
        }
    });
};

/**
 *
 */
deleteAllViajePasajero = () =>{
    let url       = "/sistema/deleteAllViajePasajero/";
    let pasajeros = {};
    $.ajax({
        type: "POST",
        url: url,
        headers: {'X-CSRFToken': csrf_token},
        data: {viaje},
        success: data => {
            //console.table(data);
            $('#grillaPasajero').html(data);
        }
    });
};


/**
 * Cris, te dejo esto del html cliente, que es de donde saqué el modal ya armado
 * @returns {boolean}
 */
guardarPasajeroModal = () => {
    if ($('#nombrePasClienteModal').val() == ""){
        showMsg("El Nombre es obligatorio.");
        return false;
    }
    if ($('#apellidoPasClienteModal').val() == ""){
        showMsg("El Apellido es obligatorio.");
        return false;
    }
    let url = "/sistema/guardarPasajeroDesdeViaje/";
    $.ajax({
        type: "POST",
        url: url,
        headers: {'X-CSRFToken': csrf_token},
        data: $("#form-datos-cliente-pasajeros").serialize(),
        success: data => {
            $('#idPasajeroModal').val("0");
            $('#nombrePasClienteModal').val("");
            $('#apellidoPasClienteModal').val("");
            $('#documentoPasajeroClienteModal').val("");
            $('#telefonoPasajeroClienteModal').val("");
            $('#mailPasajeroClienteModal').val("");
            $('#nacionalidadPasajeroClienteModal').val("");
            $('#pasajeroFrecuente').prop('checked', false);
            $('#callePasajeroClienteModal').val("");
            $('#alturaPasajeroClienteModal').val("");
            $('#pisoPasajeroClienteModal').val("");
            $('#cpPasajeroClienteModal').val("");
            $('#comentarioPasajeroClienteModal').val("");
            $('#add_pasajero').modal('toggle');
            $('#pasajero').append($('<option selected="selected">').text(data.pasajero_apellido + ' ' +data.pasajero_nombre).attr('value', data.pasajero));
            $('#pasajero_telefono').val(data.pasajero_telefono);
        }
    });
};


/**
 * Cris, te dejo esto del html cliente, que es de donde saqué el modal ya armado
 * @returns {boolean}
 */
guardarPasajero = () => {
    if ($('#nombrePasCliente').val() == ''){
        showMsg("El Nombre es obligatorio.");
        return false;
    }
    if ($('#apellidoPasCliente').val() == ''){
        showMsg("El Apellido es obligatorio.");
        return false;
    }
    let url = "/sistema/guardarPasajeroProspect/";
    $.ajax({
        type: "POST",
        url: url,
        headers: {'X-CSRFToken': csrf_token},
        data: $("#form-viaje-pasajeros").serialize(),
        success: data => {
            $('#idPasajero').val("0");
            $('#nombrePasCliente').val("");
            $('#apellidoPasCliente').val("");
            $('#documentoPasajeroCliente').val("");
            $('#telefonoPasajeroCliente').val("");
            $('#mailPasajeroCliente').val("");
            $('#nacionalidadPasajeroCliente').val("");
            $('#callePasajeroCliente').val("");
            $('#alturaPasajeroCliente').val("");
            $('#pisoPasajeroCliente').val("");
            $('#cpPasajeroCliente').val("");
            $('#comentarioPasajeroCliente').val("");
            $('#add_pasajero_cliente').modal('toggle');
            $('#grillaPasajero').html(data);
        }
    });
};

/**
 *
 * @param name
 * @param evt
 */
updateFillsByCliente = (name, evt) => {
    let url = "/sistema/getClienteById/";
    $.ajax({
        type: "POST",
        url: url,
        headers: {'X-CSRFToken': csrf_token},
        data: {cliente_id:evt.params.data.id, pasajero:pasajero},
        success: function(data)
        {
            let cliente = {};
            cliente.id = data.id;
            cliente.calle = data.calle ? data.calle : '';
            cliente.altura = data.altura ? data.altura : '';
            cliente.piso = data.piso ? data.piso : '';
            cliente.depto = data.depto ? data.depto : '';
            cliente.direccion = data.calle + ' ' + cliente.altura + ' ' + cliente.piso + ' ' + cliente.depto;
            cliente.telefono = data.telefono;
            cliente.moroso = data.moroso;
            cliente.personascliente = data.personascliente;
            cliente.centro_costos = data.centro_costos;
            //console.log(cliente.moroso)
            if(cliente.moroso === true){
                showMsg('Comunicarse con administración, cliente inhabilitado.');
            }

            //$('#id_cliente').select2('val',cliente.id);
            $('#idClienteEnSol').val(cliente.id);
            $('#idClienteEnCC').val(cliente.id);
            $('#idClientePasajeroModal').val(cliente.id);
            $('#idClientePasajero').val(cliente.id);
            $('#id_cliente').val(cliente.id).trigger('change');
            $('#cliente_direccion').val(cliente.direccion);
            $('#cliente_categoria').val(cliente.categoria_id);
            $('#cliente_tel').val(cliente.telefono);

            $('#centroDeCosto').empty().append($('<option>').text('').attr('value', ''));
            $('#contacto').empty().append($('<option>').text('').attr('value', ''));
            $('#pasajero').empty().append($('<option>').text('').attr('value', ''));
            $('#pasajero_telefono').empty().append($('<option>').text('').attr('value', ''));
            $('#pasajero_trayecto').empty().append($('<option>').text('').attr('value', ''));
            $('#suma_pasajero').empty();

            if(evt.params.data.no_borrar_pasajeros){

            }else{
                if(es_nuevo != 1){
                    deleteAllViajePasajero();
                }
            }

            $.each(cliente.centro_costos, (i, value) => {
                if(value.id == centro_costo){
                    $('#centroDeCosto').append($('<option selected="selected">').text(value.nombre).attr('value', value.id));
                }else{
                    $('#centroDeCosto').append($('<option>').text(value.nombre).attr('value', value.id));
                }
            });

            $.each(cliente.personascliente, (i, value) => {
                if(value.tipo_persona === 'Solicitante'){
                    if(value.id == solicitante){
                        $('#contacto').append($('<option selected="selected">').text(value.nombre).attr('value', value.id))
                    }else{
                        $('#contacto').append($('<option>').text(value.nombre).attr('value', value.id));
                    }
                }else if(value.tipo_persona === 'Pasajero'){
                    if(value.id == pasajero){
                        $('#pasajero').append($('<option selected="selected">').text(value.nombre).attr('value', value.id));
                        $('#pasajero_telefono').val(value.telefono);
                    }else{
                        $('#pasajero').append($('<option>').text(value.nombre).attr('value', value.id));
                    }
                    if(value.id != $('#pasajero').val()){
                        $('#suma_pasajero').append($('<option>').text(value.nombre).attr('value', value.id));
                    }

                    $('#pasajero_trayecto').append($('<option>').text(value.nombre).attr('value', value.id));
                }
            });
        }
    });
};


/**
 *
 * @param name
 * @param evt
 */
updateFillsByUnidad = (name, evt) => {
    var option_selected = evt.params.data.id;
    $('#unidad_id').select2('val',unidades[option_selected].id);
    $('#unidad_id').val(unidades[option_selected].id).trigger("change");
};

/**
 *
 * @param name
 * @param evt
 */
updateFillsByLocalidad = (name, evt) => {
    //console.log('QUE PASA')
    var localidad_id = evt.params.data.id,
        init = evt.params.data.init,
        html_select = evt.currentTarget.id,
        html_direccion = '',
        html_vuelo = '';

    switch(html_select) {
        case 'desde_localidad':
            html_direccion = 'desde_direccion';
            html_vuelo = 'desde_vuelo';
            if(!init){
                $('#desde_calle').val('');
                $('#desde_entre').val('');
                $('#desde_altura').val('');
                $('#desde_compania').val('');
                $('#desde_vuelo').val('');
            }
            break;
        case 'hasta_localidad':
            html_direccion = 'hasta_direccion';
            html_vuelo = 'hasta_vuelo';
            if(!init) {
                $('#hasta_calle').val('');
                $('#hasta_entre').val('');
                $('#hasta_altura').val('');
                $('#hasta_compania').val('');
                $('#hasta_vuelo').val('');
            }
            break;
        case 'modal_desde_localidad':
            html_direccion = 'modal_desde_direccion';
            html_vuelo = 'modal_desde_vuelo';
            if(!init) {
                $('#modal_desde_calle').val('');
                $('#modal_desde_entre').val('');
                $('#modal_desde_altura').val('');
                $('#modal_desde_compania').val('');
                $('#modal_desde_vuelo').val('');
            }
            break;
        case 'modal_hasta_localidad':
            html_direccion = 'modal_hasta_direccion';
            html_vuelo = 'modal_hasta_vuelo';
            if(!init) {
                $('#modal_hasta_calle').val('');
                $('#modal_hasta_entre').val('');
                $('#modal_hasta_altura').val('');
                $('#modal_hasta_compania').val('');
                $('#modal_hasta_vuelo').val('');
            }
            break;
    }

    checkLocalidadFlag(localidad_id, html_direccion, html_vuelo);
};

checkLocalidadFlag = (localidad_id, html_direccion, html_vuelo) => {
    let url = "/sistema/checkLocalidadFlag/";
        let param = {};
        param.localidad_id = localidad_id;
        $.ajax({
            type: "POST",
            url: url,
            headers: {'X-CSRFToken': csrf_token},
            data: param,
            success:  data => {
                console.log(data.terminal_flag)
                if(data.terminal_flag === true){
                    $("." + html_direccion).hide();
                    $("." + html_vuelo).show();
                }else{
                    $('.' + html_direccion).show();
                    $("." + html_vuelo).hide();
                }
            }
        });
};

/**
 *
 * @param name
 * @param evt
 */
updateFillsByDestino = (name, evt) => {
    var destino_id          = evt.params.data.id,
        localidad_select_id = evt.params.data.localidad_select_id,
        provincia_select_id = evt.params.data.provincia_select_id,
        init                = evt.params.data.init,
        html_select         = evt.currentTarget.id,
        html_to_change      = '',
        html_direccion      = '',
        html_vuelo          = '',
        html_cont_localidad = '',
        html_cont_provincia = '';

    switch(html_select) {
        case 'desde_destino':
            html_to_change = 'desde_localidad';
            html_direccion = 'desde_direccion';
            html_vuelo = 'desde_vuelo';
            html_cont_localidad = 'cont_desde_localidad';
            html_cont_provincia = 'cont_desde_provincia';
            if(!init){
                $('#desde_calle').val('');
                $('#desde_entre').val('');
                $('#desde_altura').val('');
                $('#desde_compania').val('');
                $('#desde_vuelo').val('');
                $('#desde_localidad').val('');
                $('#desde_provincia').val('');
            }
            break;
        case 'hasta_destino':
            html_to_change = 'hasta_localidad';
            html_direccion = 'hasta_direccion';
            html_vuelo = 'hasta_vuelo';
            html_cont_localidad = 'cont_hasta_localidad';
            html_cont_provincia = 'cont_hasta_provincia';
            if(!init) {
                $('#hasta_calle').val('');
                $('#hasta_entre').val('');
                $('#hasta_altura').val('');
                $('#hasta_compania').val('');
                $('#hasta_vuelo').val('');
                $('#hasta_localidad').val('');
                $('#hasta_provincia').val('');
            }
            break;
        case 'modal_desde_destino':
            html_to_change = 'modal_desde_localidad';
            html_direccion = 'modal_desde_direccion';
            html_vuelo = 'modal_desde_vuelo';
            html_cont_localidad = 'cont_modal_desde_localidad';
            html_cont_provincia = 'cont_modal_desde_provincia';
            if(!init) {
                $('#modal_desde_calle').val('');
                $('#modal_desde_entre').val('');
                $('#modal_desde_altura').val('');
                $('#modal_desde_compania').val('');
                $('#modal_desde_vuelo').val('');
                $('#modal_desde_localidad').val('');
                $('#modal_desde_provincia').val('');
            }
            break;
        case 'modal_hasta_destino':
            html_to_change = 'modal_hasta_localidad';
            html_direccion = 'modal_hasta_direccion';
            html_vuelo = 'modal_hasta_vuelo';
            html_cont_localidad = 'cont_modal_hasta_localidad';
            html_cont_provincia = 'cont_modal_hasta_provincia';
            if(!init) {
                $('#modal_hasta_calle').val('');
                $('#modal_hasta_entre').val('');
                $('#modal_hasta_altura').val('');
                $('#modal_hasta_compania').val('');
                $('#modal_hasta_vuelo').val('');
                $('#modal_hasta_localidad').val('');
                $('#modal_hasta_provincia').val('');
            }
            break;
    }

    if(destino_id == 1 || destino_id == 2){
        $('.' + html_direccion).show();
        $("." + html_vuelo).hide();
        $("." + html_cont_localidad).show();
        $("." + html_cont_provincia).hide();
    }/*else if(destino_id == 9){
        $("." + html_direccion).hide();
        $("." + html_vuelo).show();
        $("." + html_cont_localidad).hide();
        $("." + html_cont_provincia).hide();
    }*/

    if(destino_id != '' && destino_id != ''){
        var url = "/sistema/cargarLocalidadByDestino/";
        var param = {};
        param.destino_id = destino_id;
        param.localidad_select_id = localidad_select_id;
        $.ajax({
            type: "POST",
            url: url,
            headers: {'X-CSRFToken': csrf_token},
            data: param,
            success:  data => {
                $('#' + html_to_change).html(data);
            }
        });
    }
};

/**
 *
 */
agregarTramo = () => {
    console.log(viaje);
    if(!viaje){
        showMsg('Debes guardar el viaje antes de crear un tramo');
        return;
    }

    let obj               = {};
    obj.desde_destino     = $("#modal_desde_destino").val();
    obj.desde_localidad   = $("#modal_desde_localidad").val();
    obj.desde_provincia   = $("#modal_desde_provincia").val();
    obj.desde_calle       = $("#modal_desde_calle").val();
    obj.desde_altura      = $("#modal_desde_altura").val();
    obj.desde_entre       = $("#modal_desde_entre").val();
    obj.desde_compania    = $("#modal_desde_compania").val();
    obj.desde_vuelo       = $("#modal_desde_vuelo").val();
    obj.hasta_destino     = $("#modal_hasta_destino").val();
    obj.hasta_localidad   = $("#modal_hasta_localidad").val();
    obj.hasta_provincia   = $("#modal_hasta_provincia").val();
    obj.hasta_altura      = $("#modal_hasta_altura").val();
    obj.hasta_calle       = $("#modal_hasta_calle").val();
    obj.hasta_entre       = $("#modal_hasta_entre").val();
    obj.hasta_compania    = $("#modal_hasta_compania").val();
    obj.hasta_vuelo       = $("#modal_hasta_vuelo").val();
    obj.pasajero          = $("#pasajero_trayecto").val();
    obj.principal         = 0;
    obj.idViaje           = viaje;
    obj.id                = $("#modal_id").val();


    let url = "/sistema/guardarTrayecto/"; // the script where you handle the form input.
    $.ajax({
       type: "POST",
       url: url,
       headers: {'X-CSRFToken': csrf_token},
       data: obj, // serializes the form's elements.
       success:  data => {
           if(data.error == '1'){
               showMsg(data.msg);
           }else{
               $("#grillaTramos").html(data);
               $('#add_tramo').modal('toggle');
           }
       }
     });
};

/**
 *
 */
agregarObservacion = () => {
    if ($('#textAreaObservacion').val() == ""){
        showMsg("Campo observacion es obligatorio", 'error');
    }else if($("#idViajeObser").val() == 0){
        showMsg("Debes crear el viaje antes.", 'error');
    }else{
        let url = "/sistema/guardarObservacionViaje/";
        $.ajax({
            type: "POST",
            url: url,
            data: $("#form-datos-viaje-observacion").serialize(),
            success: data => {
                $("#grillaObservaciones").html(data);
                $('#add_observacion_viaje').modal('toggle');
                $('#texto_obs').val('')
            }
        });
    }
};

/**
 *
 */
fillViajeItems = () => {
    let sum_total_proveedor = 0;
    let sum_total_cliente = 0;
    viaje_items.forEach(value => {
        //console.log(value.monto_s_iva);
        switch(value.tipo_items_viaje){
            case '1':
                $('#admin_espera_cliente').val(value.monto_s_iva);
                $('#admin_cant_espera_cliente').val(value.cant);
                sum_total_cliente += parseFloat(value.monto_s_iva);
            break;              
            case '2':
                $('#admin_costo_cliente').val(parseFloat(value.monto_s_iva));
                sum_total_cliente += parseFloat(value.monto_s_iva);
            break;              
            case '3':

                if(value.cant == 1){
                    $('#admin_bilingue_cliente').prop('checked', true);
                }
                $('#admin_costo_bilingue_cliente').val(parseFloat(value.monto_s_iva));
                sum_total_cliente += parseFloat(value.monto_s_iva);
            break;            
            case '4':
                $('#admin_costo_maletas_cliente').val(parseFloat(value.monto_s_iva));
                $('#admin_cant_maletas_cliente').val(value.cant);
                sum_total_cliente += parseFloat(value.monto_s_iva);
            break;          
            case '5':
                $('#admin_estacionamiento_cliente').val(parseFloat(value.monto_s_iva));
                sum_total_cliente += parseFloat(value.monto_s_iva);
            break;
            case '6':
                $('#admin_peaje_cliente').val(parseFloat(value.monto_s_iva));
                sum_total_cliente += parseFloat(value.monto_s_iva);
            break;                
            case '8':
                $('#admin_costo_proveedor').val(parseFloat(value.monto_s_iva));
                sum_total_proveedor += parseFloat(value.monto_s_iva);
            break;
            case '9':
                if(value.cant == 1){
                    $('#admin_bilingue_proveedor').prop('checked', true);
                }
                $('#admin_costo_bilingue_proveedor').val(parseFloat(value.monto_s_iva));
                sum_total_proveedor += parseFloat(value.monto_s_iva);
            break;
            case '10':
                $('#admin_cant_maletas_proveedor').val(value.cant);
                $('#admin_costo_maletas_proveedor').val(parseFloat(value.monto_s_iva));
                sum_total_proveedor += parseFloat(value.monto_s_iva);
            break;
            case '11':
                $('#admin_estacionamiento_proveedor').val(parseFloat(value.monto_s_iva));
                sum_total_proveedor += parseFloat(value.monto_s_iva);
            break;
            case '12':
                $('#importe_efectivo').val(parseFloat(value.monto_s_iva));
            break;
            case '13':
                $('#admin_hs_dispo_proveedor').val(parseFloat(value.monto_s_iva));
                $('#admin_cant_hs_dispo_proveedor').val(value.cant);
                sum_total_proveedor += parseFloat(value.monto_s_iva);
            break;
            case '14':
                $('#admin_espera_proveedor').val(value.monto_s_iva);
                $('#admin_cant_espera_proveedor').val(value.cant);
                sum_total_proveedor += parseFloat(value.monto_s_iva);
            break;
            case '15':
                $('#admin_peaje_proveedor').val(parseFloat(value.monto_s_iva));
                sum_total_proveedor += parseFloat(value.monto_s_iva);
            break;
            case '16':
                $('#admin_otros_proveedor').val(parseFloat(value.monto_s_iva));
                sum_total_proveedor += parseFloat(value.monto_s_iva);
            break;
            case '17':
                $('#admin_otros_cliente').val(parseFloat(value.monto_s_iva));
                sum_total_cliente += parseFloat(value.monto_s_iva);
            break;            
            case '18':
                $('#admin_hs_dispo_cliente').val(parseFloat(value.monto_s_iva));
                $('#admin_cant_hs_dispo_cliente').val(value.cant);
                sum_total_cliente += parseFloat(value.monto_s_iva);
            break;
            default:
        }        
    });
    $('#admin_total_cliente').val(sum_total_cliente);
    $('#admin_total_proveedor').val(sum_total_proveedor);
};

/**
 *
 */
guardaAdjuntoViaje = () =>{
    var formData = new FormData();
    formData.append('file', $('#file')[0].files[0]);

    $.ajax({
           url : '/sistema/guardarViajeAdjunto/?idViaje={{ viaje.id }}',
           type : 'POST',
           data : formData,
           processData: false,  // tell jQuery not to process the data
           contentType: false,  // tell jQuery not to set contentType
           success : function(data) {
               console.log(data);
               alert(data);
           }
    });
};

/**
 *
 * @returns {boolean}
 */
guardarCentroCosto = () =>{
    if ($('#codigoCCCliente').val() == ""){
        showMsg("El Codigo es obligatorio.", 'error');
        return false;
    }
    if ($('#desdeCC').val() == ""){
        showMsg("La fecha desde es obligatoria.", 'error');
        return false;
    }

    if ($("#idClienteCC").val() == "0"){
        let url = "/sistema/validarCodigoCentroCosto/?codigoCC="+$("#codigoCCCliente").val();
        $.ajax({
            type: "GET",
            url: url,
            success: function(data){
                if (data.mensaje === ""){
                    guardarCCmetodo()
                }else{
                    showMsg(data.mensaje, 'error');
                }

            }
        });
    }else{
        guardarCCmetodo()
    }
};

/**
 *
 */
guardarCCmetodo = () =>{
    let url = "/sistema/guardarCentroCostoProspectDesdeViaje/";
    $.ajax({
        type: "POST",
        url: url,
        headers: {'X-CSRFToken': csrf_token},
        data: $("#form-datos-centro-de-costo").serialize(),
        success: function(data){
            $('#codigoCCCliente').val("");
            $('#descripcionCCCliente').val("");
            $('#selectTarifariosCCCliente').val("");
            $('#desdeCC').val("");
            $('#hastaCC').val("");
            $("#centroDeCosto").html(data);
            $('#add_centro_costo').modal('toggle');
        }
    });
};

//Se utiliza para que el campo de texto solo acepte letras
/**
 *
 * @param e
 * @returns {boolean}
 */
soloLetras = e =>{
    key = e.keyCode || e.which;
    tecla = String.fromCharCode(key).toString();
    letras = "áéíóúabcdefghijklmnñopqrstuvwxyzÁÉÍÓÚABCDEFGHIJKLMNÑOPQRSTUVWXYZ0123456789";//Se define todo el abecedario que se quiere que se muestre.
    especiales = [8, 39, 6]; //Es la validación del KeyCodes, que teclas recibe el campo de texto.
    tecla_especial = false
    for(var i in especiales) {
        if(key == especiales[i]) {
            tecla_especial = true;
            break;
        }
    }

    if(letras.indexOf(tecla) == -1 && !tecla_especial){
        return false;
    }
}

mailto = () =>{
    let url = "/sistema/mailtoViaje/";
    $.ajax({
        type: "POST",
        url: url,
        data: "idViaje="+$("#idViajeObser").val(),
        headers: {'X-CSRFToken': csrf_token},
        success: function(data){
            hrefmailto = "mailto:"+data['mailto']+"?subject="+data['subject']+"&bcc="+data['mailtocco']+"&body="+data['body']
            window.location.href = hrefmailto;
        }
    });
}