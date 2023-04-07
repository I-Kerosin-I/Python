let VSHADER_SOURCE = document.getElementById('VSHADER').textContent
let FSHADER_SOURCE = document.getElementById('FSHADER').textContent

function getShader(gl, id, src) {
    if (id === 'vs') {
        shader = gl.createShader(gl.VERTEX_SHADER)
    } else if (id === 'fs') {
        shader = gl.createShader(gl.FRAGMENT_SHADER)
    } else {
        return null
    }

    gl.shaderSource(shader, src)
    gl.compileShader(shader)

    if (!gl.getShaderParameter(shader, gl.COMPILE_STATUS)) {
        alert('пиздец')
        console.log(gl.getShaderInfoLog(shader))
        return null
    }
    return shader
}

function initShaders(gl) {
    let VS = getShader(gl, 'vs', VSHADER_SOURCE)
    let FS = getShader(gl, 'fs', FSHADER_SOURCE)

    shaderProgram = gl.createProgram()
    gl.attachShader(shaderProgram, VS)
    gl.attachShader(shaderProgram, FS)
    gl.linkProgram(shaderProgram)
    gl.useProgram(shaderProgram)
}

function webGL_start() {
    let canv = document.getElementById('gl_canvas')
    canv.height = document.documentElement.clientHeight
    canv.width = document.documentElement.clientWidth

    let gl = canv.getContext('webgl')

    initShaders(gl)

    gl.clearColor(0.1, 0.1, 0.1, 1)

    //----------------------- Variables -----------------------//
    let a_Color = gl.getAttribLocation(shaderProgram, 'a_Color')
    let a_Position = gl.getAttribLocation(shaderProgram, 'a_Position')

    gl.enableVertexAttribArray(a_Color)
    gl.enableVertexAttribArray(a_Position)

    let triangle_vertex = [
        Math.random()*2-1, Math.random()*2-1, Math.random(), Math.random(), Math.random(),
        Math.random()*2-1, Math.random()*2-1, Math.random(), Math.random(), Math.random(),
        Math.random()*2-1, Math.random()*2-1, Math.random(), Math.random(), Math.random(),
        Math.random()*2-1, Math.random()*2-1, Math.random(), Math.random(), Math.random()]
    // let triangle_vertex = [
    //     Math.random()*2-1, Math.random()*2-1, 1.0, 1.0, 1.0,
    //     Math.random()*2-1, Math.random()*2-1, 1.0, 0.0, 0.0,
    //     Math.random()*2-1, Math.random()*2-1, 0.0, 1.0, 0.0,
    //     Math.random()*2-1, Math.random()*2-1, 0.0, 0.0, 1.0]

    let TRIANGLE_VERTEX = gl.createBuffer()
    gl.bindBuffer(gl.ARRAY_BUFFER, TRIANGLE_VERTEX)
    gl.bufferData(gl.ARRAY_BUFFER, new Float32Array(triangle_vertex), gl.STATIC_DRAW)

    gl.vertexAttribPointer(a_Position, 2, gl.FLOAT, false, 20, 0)
    gl.vertexAttribPointer(a_Color, 3, gl.FLOAT, false, 20, 8)

    let TRIANGLE_FACES = gl.createBuffer()
    gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER, TRIANGLE_FACES)
    gl.bufferData(gl.ELEMENT_ARRAY_BUFFER, new Uint16Array([0,1,2, 0,2,3]), gl.DYNAMIC_DRAW)

    function draw() {

        gl.clear(gl.COLOR_BUFFER_BIT)

        gl.drawElements(gl.TRIANGLES, 6, gl.UNSIGNED_SHORT, 0)
        gl.flush()
    }

    document.getElementsByTagName("body")[0].onresize = (ev) => {
        canv.height = document.documentElement.clientHeight
        canv.width = document.documentElement.clientWidth
        draw()
    }

    // canv.onresize = () => {draw()}
    canv.onmousemove = (ev) => {
        triangle_vertex[0] = ev.clientX / canv.width * 2 - 1
        triangle_vertex[1] = 1 - ev.clientY / canv.height * 2
        gl.bindBuffer(gl.ARRAY_BUFFER, TRIANGLE_VERTEX)
        gl.bufferData(gl.ARRAY_BUFFER, new Float32Array(triangle_vertex), gl.DYNAMIC_DRAW)
        draw()
    }


    // gl.drawArrays(gl.TRIANGLES, 0, 3)


    //---------------------------------------------------------//


    // gl.drawArrays(gl.POINTS, 0, 1)
}