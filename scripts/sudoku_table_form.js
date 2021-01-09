const form_s = document.getElementById('s');

function submit(data) {
    let form = document.createElement("form")
    form.setAttribute("method", "post")
    form.setAttribute("action", "/solve")

    let data_input = document.createElement("input")
    data_input.setAttribute("type", "hidden")
    data_input.setAttribute("name", "data")
    data_input.setAttribute("value", JSON.stringify(data))
    form.appendChild(data_input)

    document.body.appendChild(form)
    form.submit()
}

form_s.addEventListener('submit', (evt) => {
    evt.preventDefault()
    let data = [];
    let fd = new FormData(evt.target)
    for (let ff_key of fd.keys()) {
        let [r, c] = ff_key.split(',')
        let ff_val = fd.get(ff_key)
        if ('string' != typeof ff_val || !ff_val) {
            continue
        }
        ff_val = parseInt(ff_val, 10)
        data.push([parseInt(r, 10), parseInt(c, 10), ff_val])
    }

    submit(data)
});
