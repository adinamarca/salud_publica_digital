function getCookie(cname) {
    var name = cname + "=";
    var ca = document.cookie.split(';');
    for(var i=0; i<ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0)==' ') c = c.substring(1);
        if(c.indexOf(name) == 0)
            return c.substring(name.length,c.length);
    }
    return "";
}

document.addEventListener('DOMContentLoaded', function() {
    const regionSelect = document.getElementById('region');
    const comunaSelect = document.getElementById('comuna');
    const consultorioSelect = document.getElementById('consultorio');

    regionSelect.addEventListener('change', function() {
        const regionId = parseInt(this.value);
        if (regionId) {
            fetch(`/api/v1/comuna/${regionId}/`,
            {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                }
            })
                .then(response => response.json())
                .then(data => {
                    comunaSelect.innerHTML = '<option value="">Seleccione una comuna</option>';
                    data.forEach(comuna => {
                        comunaSelect.innerHTML += `<option value="${comuna.c_com}">${comuna.nom_com}</option>`;
                    });
                    comunaSelect.disabled = false;
                });
        } else {
            comunaSelect.innerHTML = '<option value="">Seleccione una comuna</option>';
            comunaSelect.disabled = true;
            consultorioSelect.innerHTML = '<option value="">Seleccione un consultorio</option>';
            consultorioSelect.disabled = true;
        }
    });

    comunaSelect.addEventListener('change', function() {
        const comunaId = this.value;
        if (comunaId) {
            fetch(`/api/v1/consultorio/${comunaId}/`,
            {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                }
            })
                .then(response => response.json())
                .then(data => {
                    consultorioSelect.innerHTML = '<option value="">Seleccione un consultorio</option>';
                    data.forEach(consultorio => {
                        consultorioSelect.innerHTML += `<option value="${consultorio.objectid}">${consultorio.nombre}</option>`;
                    });
                    consultorioSelect.disabled = false;
                });
        } else {
            consultorioSelect.innerHTML = '<option value="">Seleccione un consultorio</option>';
            consultorioSelect.disabled = true;
        }
    });
});