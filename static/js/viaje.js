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

    $(".cont_desde_provincia").hide();
    $(".cont_hasta_provincia").hide();
    $(".cont_modal_desde_provincia").hide();
    $(".cont_modal_hasta_provincia").hide();
    $(".hasta_vuelo").hide();
    $(".desde_vuelo").hide();
    $(".modal_desde_vuelo").hide();
    $(".modal_hasta_vuelo").hide();

    if(es_nuevo == '1'){
        $('#fecha').datepicker('setDate', 'today');
        $("#viaje-tab").hide();
        $('#estado').attr("disabled", true);
    }else{
        $("#viaje-tab").show();
        if(mensaje != ''){showMsg(mensaje, 'success')}
        $('#viaje_titulo').html('Ingreso del Cliente y Datos del Viaje ' + viaje);
        //HAGO ESTO PARA SIMULAR UN EVENTO QUE PIDE LA FUNCION DE SELECT2ME
        var evt = {};

        evt.params = {};
        evt.params.data = {};
        evt.params.data.id = cliente_id;
        updateFillsByCliente('', evt);

        evt.params.data.id = destino_desde_id;
        evt.params.data.provincia_select_id = provincia_desde_id;
        evt.params.data.localidad_select_id = localidad_desde_id;
        evt.params.data.init = true;
        evt.currentTarget = {};
        evt.currentTarget.id = 'desde_destino';
        updateFillsByDestino('', evt);

        evt.currentTarget.id = 'desde_localidad';
        evt.params.data.id = localidad_desde_id;
        updateFillsByLocalidad('', evt);

        evt.params.data.id = destino_hasta_id;
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
    }

    $("#id_cliente").on("select2:select", function (e) { updateFillsByCliente("select2:select", e); });
    $('#id_cliente').select2({ placeholder: 'Seleccionar Cliente', dropdownAutoWidth : true, width: 'auto'});
    $("#unidad_id").on("select2:select", function (e) { updateFillsByUnidad("select2:select", e); });
    $('#unidad_id').select2({placeholder: 'Seleccionar', dropdownAutoWidth : true, width: 'auto'});
    $('#centro_costos').select2({placeholder: 'Seleccionar', dropdownAutoWidth : true, width: 'auto'});


    $("#desde_destino").on("select2:select", function (e) { updateFillsByDestino("select2:select", e); });
    $('#desde_destino').select2({placeholder: 'Seleccionar', dropdownAutoWidth : true, width: 'auto'});
    $("#hasta_destino").on("select2:select", function (e) { updateFillsByDestino("select2:select", e); });
    $('#hasta_destino').select2({placeholder: 'Seleccionar', dropdownAutoWidth : true, width: 'auto'});
    $("#modal_desde_destino").on("select2:select", function (e) { updateFillsByDestino("select2:select", e); });
    $('#modal_desde_destino').select2({placeholder: 'Seleccionar', dropdownAutoWidth : true, width: 'auto'});
    $("#modal_hasta_destino").on("select2:select", function (e) { updateFillsByDestino("select2:select", e); });
    $('#modal_hasta_destino').select2({placeholder: 'Seleccionar', dropdownAutoWidth : true, width: 'auto'});

    $("#desde_localidad").on("select2:select", function (e) { updateFillsByLocalidad("select2:select", e); });
    $('#desde_localidad').select2({placeholder: 'Seleccionar', dropdownAutoWidth : true, width: 'auto'});
    $("#hasta_localidad").on("select2:select", function (e) { updateFillsByLocalidad("select2:select", e); });
    $('#hasta_localidad').select2({placeholder: 'Seleccionar', dropdownAutoWidth : true, width: 'auto'});
    $("#modal_desde_localidad").on("select2:select", function (e) { updateFillsByLocalidad("select2:select", e); });
    $('#modal_desde_localidad').select2({placeholder: 'Seleccionar', dropdownAutoWidth : true, width: 'auto'});
    $("#modal_hasta_localidad").on("select2:select", function (e) { updateFillsByLocalidad("select2:select", e); });
    $('#modal_hasta_localidad').select2({placeholder: 'Seleccionar', dropdownAutoWidth : true, width: 'auto'});

    var tmp_tipo_observacion;
    $('#tipo_viaje_obs').append($('<option>').text('').attr('value', ''));
    $.each(tipo_observaciones, (i, value) => {
        if(tmp_tipo_observacion != value.tipo_observacion){
            $('#tipo_viaje_obs').append($('<option>').text(value.tipo_observacion).attr('value', value.tipo_observacion));
        }
        tmp_tipo_observacion = value.tipo_observacion;
    });

    $('#tipo_viaje_obs').on('change', e => {
        var optionSelected = $("option:selected", this);
        var valueSelected = this.value;
        $('#detalle_obs').empty();

        $.each(tipo_observaciones, (i, value) => {
            if(valueSelected == value.tipo_observacion){
              $('#detalle_obs').append($('<option>').text(value.detalle_tipo_obs).attr('value', value.id));
            }
        });
    });

    $("#form-viaje-viaje").submit( e => {
        if ($("#id_cliente").val() == ""){
            showMsg("El campo cliente es obligatorio.");
            return false;
        }
        if ($("#contacto").val() == ""){
            showMsg("El campo solicitante es obligatorio.");
            return false;
        }
        if ($("#centro_costos").val() == ""){
            showMsg("El campo centro de costo es obligatorio.");
            return false;
        }
        if ($("#pasajero").val() == ""){
            showMsg("El campo pasajero es obligatorio.");
            return false;
        }
        if ($("#fecha").val() == ""){
            showMsg("El campo fecha es obligatorio.");
            return false;
        }
        if ($("#hora").val() == ""){
            showMsg("El campo hora es obligatorio.");
            return false;
        }
        if ($("#hora_estimada").val() == ""){
            showMsg("El campo hora estimada es obligatorio.");
            return false;
        }
        if ($("#categoria_viaje").val() == ""){
            showMsg("El campo categoria viaje es obligatorio.");
            return false;
        }
        if(es_nuevo != '1'){
            if ($("#unidad_id").val() == ""){
                showMsg("El campo unidad es obligatorio.");
                return false;
            }
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
        obj.centro_costos     = $("#centro_costos").val();
        obj.pasajero          = $("#pasajero").val();
        obj.fecha             = $("#fecha").val();
        obj.hora              = $("#hora").val();
        obj.hora_estimada     = $("#hora_estimada").val();
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
        obj.maletas           = $("#maletas:checked").val() || '';
        obj.costo_maletas     = $("#costo_maletas").val();
        obj.bilingue          = $("#bilingue:checked").val() || '';
        obj.costo_bilingue    = $("#costo_bilingue").val();
        obj.cod_externo       = $("#cod_externo").val();
        obj.nro_aux           = $("#nro_aux").val();
        obj.tipo_pago         = $("#tipo_pago").val();
        obj.importe_efectivo  = $("#importe_efectivo").val();
        obj.tiempo_hs_dispo   = $("#tiempo_hs_dispo").val();
        obj.hs_dispo          = $("#hs_dispo").val();
        obj.es_nuevo          = es_nuevo;

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
              data.url ? window.location.replace(data.url) : showMsg(data.msg, 'success');
           }
        });

        e.preventDefault(); // avoid to execute the actual submit of the form.
    });

    $("#form-viaje-trayecto").submit( e => {
        /*if ($("#desde_destino").val() == ""){
            showMsg("El campo desde destino es obligatorio.");
            return false;
        }
        if ($("#desde_localidad").val() == ""){
            showMsg("El campo desde localidad es obligatorio.");
            return false;
        }
        if ($("#hasta_destino").val() == ""){
            showMsg("El campo hasta destino es obligatorio.");
            return false;
        }
        if ($("#hasta_localidad").val() == ""){
            showMsg("El campo hasta localidad es obligatorio.");
            return false;
        }*/

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
    });

    $(document).on( "click", '.delete_button', e => {
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

        $("#modal_desde_destino").val('');
        $("#modal_desde_provincia").val('');
        $("#modal_desde_localidad").val('');
        $("#modal_hasta_destino").val('');
        $("#modal_hasta_provincia").val('');
        $("#modal_hasta_localidad").val('');

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
    });

    $(document).on( "click", '.edit_button', e => {

        var id              = $(this).data('id');

        var provincia_desde = $(this).data('provincia_desde');
        var localidad_desde = $(this).data('localidad_desde');
        var destino_desde   = $(this).data('destino_desde');
        var provincia_hasta = $(this).data('provincia_hasta');
        var localidad_hasta = $(this).data('localidad_hasta');
        var destino_hasta   = $(this).data('destino_hasta');

        var calle_desde     = $(this).data('calle_desde');
        var altura_desde    = $(this).data('altura_desde');
        var entre_desde     = $(this).data('entre_desde');
        var compania_desde  = $(this).data('compania_desde');
        var vuelo_desde     = $(this).data('vuelo_desde');
        var calle_hasta     = $(this).data('calle_hasta');
        var altura_hasta    = $(this).data('altura_hasta');
        var entre_hasta     = $(this).data('entre_hasta');
        var compania_hasta  = $(this).data('compania_hasta');
        var vuelo_hasta     = $(this).data('vuelo_hasta');

        $("#modal_id").val(id);

        $("#modal_desde_destino").val(destino_desde);
        $("#modal_desde_localidad").val(localidad_desde);
        $("#modal_desde_provincia").val(provincia_desde);
        $("#modal_hasta_destino").val(destino_hasta);
        $("#modal_hasta_localidad").val(localidad_hasta);
        $("#modal_hasta_provincia").val(provincia_hasta);

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

        //$(".modal-title").text('Editar Tramo');
    });

    $( "#pasajero" ).change(updateFillsByPasajero);

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

/*Cris, te dejo esto del html cliente, que es de donde saqué el modal ya armado*/
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

sumarPasajero = () => {
    let url = "/sistema/guardaViajePasajeroPOST/";
    $.ajax({
        type: "POST",
        url: url,
        headers: {'X-CSRFToken': csrf_token},
        data: {pasajero:$('#suma_pasajero').val(), viaje},
        success: data => {
            showMsg('Agregado con exito', 'success')
            $('#grillaPasajero').html(data);
        }
    });
    
}

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

updateFillsByPasajero = () =>{
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
};

deleteViajePasajero = pasajero_id =>{
    let url       = "/sistema/deleteViajePasajero/";
    let pasajeros = {};
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

 /*Cris, te dejo esto del html cliente, que es de donde saqué el modal ya armado*/
guardarPasajeroModal = () => {
    if ($('#nombrePasClienteModal').val() == ""){
        showMsg("El Nombre es obligatorio.")
        return false;
    }
    if ($('#apellidoPasClienteModal').val() == ""){
        showMsg("El Apellido es obligatorio.")
        return false;
    }
    let url = "/sistema/guardarPasajeroDesdeViaje/";
    $.ajax({
        type: "POST",
        url: url,
        headers: {'X-CSRFToken': csrf_token},
        data: $("#form-datos-cliente-pasajeros").serialize(),
        success: data => {
            $('#idPasajeroModal').val("0")
            $('#nombrePasClienteModal').val("")
            $('#apellidoPasClienteModal').val("")
            $('#documentoPasajeroClienteModal').val("")
            $('#telefonoPasajeroClienteModal').val("")
            $('#mailPasajeroClienteModal').val("")
            $('#nacionalidadPasajeroClienteModal').val("")
            $('#callePasajeroClienteModal').val("")
            $('#alturaPasajeroClienteModal').val("")
            $('#pisoPasajeroClienteModal').val("")
            $('#cpPasajeroClienteModal').val("")
            $('#comentarioPasajeroClienteModal').val("")
            $('#add_pasajero').modal('toggle');
            $('#pasajero').html(data);
        }
    });
}

 /*Cris, te dejo esto del html cliente, que es de donde saqué el modal ya armado*/
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

updateFillsByCliente = (name, evt) => {
    cliente = searchCliente(evt.params.data.id);

    $('#id_cliente').select2('val',cliente.id);
    $('#idClienteEnCC').val(cliente.id);
    $('#idClientePasajero').val(cliente.id);
    $('#id_cliente').val(cliente.id).trigger("change");
    $('#cliente_direccion').val(cliente.direccion);
    $('#cliente_categoria').val(cliente.categoria_id);
    $('#cliente_tel').val(cliente.telefono);

    $('#centro_costos').empty();
    $('#contacto').empty();
    $('#pasajero').empty();
    $('#suma_pasajero').empty();

    if(es_nuevo != 1){
        deleteAllViajePasajero();
    }

    $.each(cliente.centro_costos, (i, value) => {
      $('#centro_costos').append($('<option>').text(value.nombre).attr('value', value.id));
    });
    $.each(cliente.personascliente, (i, value) => {
        if(value.tipo_persona == 'Solicitante'){
            $('#contacto').append($('<option>').text(value.nombre).attr('value', value.id));
        }
    });
    $.each(cliente.personascliente, (i, value) => {
        if(value.tipo_persona == 'Pasajero'){
            $('#pasajero').append($('<option>').text(value.nombre).attr('value', value.id));
            if(value.id != $('#pasajero').val()){                
                $('#suma_pasajero').append($('<option>').text(value.nombre).attr('value', value.id));
            }
        }
    });
}

searchCliente = (_cliente_id) => {
    let cliente = {};
    $.each(clientes, (i, value) => {
        if(value.id == _cliente_id){
            cliente = value;
        }
    }); 
    return cliente;
}

updateFillsByUnidad = (name, evt) => {
    var option_selected = evt.params.data.id - 1;
    $('#unidad_id').select2('val',unidades[option_selected].id);
    $('#unidad_id').val(unidades[option_selected].id).trigger("change");
}

updateFillsByLocalidad = (name, evt) => {
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
        case 'modal_desde_localidad':
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

    var terminal_flag;
    $.each(localidades, function(i, value) {
        if(value.id == localidad_id){
            terminal_flag = value.terminal_flag;
        }
    });

    if(terminal_flag == 'True'){
        $("." + html_direccion).hide();
        $("." + html_vuelo).show();
    }else{
        $('.' + html_direccion).show();
        $("." + html_vuelo).hide();
    }
}
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
    }else if(destino_id == 3 ){
        $("." + html_direccion).show();
        $("." + html_vuelo).hide();
        $("." + html_cont_localidad).hide();
        $("." + html_cont_provincia).show();
    }else if(destino_id == 9/* || destino_id == 2 || destino_id == 3 || destino_id == 4 */){
        $("." + html_direccion).hide();
        $("." + html_vuelo).show();
        $("." + html_cont_localidad).hide();
        $("." + html_cont_provincia).hide();
    }

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
}

agregarTramo = () => {
    /*if ($("#modal_desde_destino").val() == ""){
        showMsg("El campo desde destino es obligatorio.");
        return false;
    }
    if ($("#modal_desde_localidad").val() == ""){
        showMsg("El campo desde localidad es obligatorio.");
        return false;
    }
    if ($("#modal_hasta_destino").val() == ""){
        showMsg("El campo hasta destino es obligatorio.");
        return false;
    }
    if ($("#modal_hasta_localidad").val() == ""){
        showMsg("El campo hasta localidad es obligatorio.");
        return false;
    }*/

    var obj               = {};
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
    obj.principal         = 0;
    obj.idViaje           = viaje;
    obj.id                = $("#modal_id").val();


    var url = "/sistema/guardarTrayecto/"; // the script where you handle the form input.
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
}
agregarObservacion = () => {
    if ($('#textAreaObservacion').val() == ""){
        showMsg("Campo observacion es obligatorio", 'error');
    }else{
        var url = "/sistema/guardarObservacionViaje/";
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
}

fillViajeItems = () => {
    viaje_items.forEach(value => {
        switch(value.tipo_items_viaje){                
            case '8':
                $('#costo_proveedor').val(parseInt(value.monto));
            break;
            case '9':
                if(value.cant == 1){
                    $('#bilingue').prop('checked', true);
                }
                $('#costo_bilingue').val(parseInt(value.monto));
            break;
            case '10':
                if(value.cant == 1){
                    $('#maletas').prop('checked', true);
                }
                $('#costo_maletas').val(parseInt(value.monto));
            break;
            case '11':
                $('#estacionamiento').val(parseInt(value.monto));
            break;
            case '12':
                $('#importe_efectivo').val(parseInt(value.monto));
            break;
            case '13':
                $('#hs_dispo').val(parseInt(value.monto));
                $('#tiempo_hs_dispo').val(value.cant);
            break;
            case '14':
                $('#espera').val(parseInt(value.monto));
                $('#tiempo_espera').val(value.cant);
            break;
            case '15':
                $('#peaje').val(parseInt(value.monto));
            break;
            case '16':
                $('#otros').val(parseInt(value.monto));
            break;
            default:

        }
    });
};

$(function() {
    'use strict';
    // Initialize the jQuery File Upload widget
    // For a complete option reference go to
    // https://github.com/blueimp/jQuery-File-Upload
    $('#fileupload').fileupload({
        // this formData is neccessary to pass the csrf and pass uid to django
        formData: [
            { name: "uid", value: uid},
            { name: "idViaje", value: viaje},
            { name: "csrfmiddlewaretoken", value: csrf_token}
        ],
        sequentialUploads: true,
        getNumberOfFiles: function () {
            return this.filesContainer.children()
                .not('.processing').length;
        },
        maxNumberOfFiles: 3,
        add: function(e, data) {
            var uploadErrors = [];
            var acceptFileTypes = /^image\/(gif|jpe?g|png)$|^application\/(pdf|msword)$|^text\/plain$/i;
            if(data.originalFiles[0]['type'].length && !acceptFileTypes.test(data.originalFiles[0]['type'])) {
                uploadErrors.push('Tipo de archivo no aceptado.');
            }
            if(data.originalFiles[0]['size'].length && data.originalFiles[0]['size'] > 3000000) {
                uploadErrors.push('Máximo 3 mb.');
            }
            if(data.files.length>=3){
                uploadErrors.push('Máximo 3 archivos.');
            }
            if(uploadErrors.length > 0) {
                showMsg(uploadErrors.join("\n"));
            } else {
                data.submit();
            }
        },
        change : function (e, data) {
            if(data.files.length>=3){
                showMsg("Máximo 3 archivos.");
                return false;
            }
        },
    });
    // Load existing files
    $.getJSON($('#fileupload form').prop('action'), function (files) {
        var fu = $('#fileupload').data('fileupload');
        fu._adjustMaxNumberOfFiles(-files.length);
        fu._renderDownload(files)
                .appendTo($('#fileupload .files'))
                .fadeIn(function () {
                    // Fix for IE7 and lower:
                    $(this).show();
                });
    });
    // Open download dialogs via iframes,
    // to prevent aborting current uploads
    $('body').on('click', '#fileupload .files a:not([target^=_blank])', function (e) {
        e.preventDefault();
        $('<iframe style="display:none;"></iframe>')
                .prop('src', this.href)
                .appendTo('body');
    });
});