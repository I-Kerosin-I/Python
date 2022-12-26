let canv = document.createElement('canvas');
canv.height = document.documentElement.clientHeight
canv.width = document.documentElement.clientWidth

const body = document.getElementsByTagName("body")[0];
body.appendChild(canv);

const ctx = canv.getContext('2d')
ctx.fillStyle = '#333333'
ctx.fillRect(0, 0, canv.width, canv.height)

const mod = (a, b) => (b + (a % b)) % b
const div = (a, b) => ((a / b) | 0)

const size = 10
let snake = [{x: 0, y: 0}]
let apple = {x: 100, y: 100}
let queue = [{dx: 1, dy: 0}]
let dx = 1, dy = 0, dx_ = 1, dy_ = 0

document.addEventListener('keydown' ,ev => {if (ev.keyCode === 107) {apple.x = snake[0].x +dx*size; apple.y = snake[0].y+dy*size;}})
document.addEventListener('keydown', (ev) =>{
    switch (ev.keyCode) {
        case 38:
            if ((queue.length > 0 ? queue[0].dy : dy) !== 1) {
                queue.unshift({dx: 0, dy: -1})
            }break
        case 40:
            if ((queue.length > 0 ? queue[0].dy : dy) !== -1) {
                queue.unshift({dx: 0, dy: 1})
            }break
        case 37:
            if ((queue.length > 0 ? queue[0].dx : dx) !== 1) {
                queue.unshift({dx: -1, dy: 0})
            }break
        case 39:
            if ((queue.length > 0 ? queue[0].dx : dx) !== -1) {
                queue.unshift({dx: 1, dy: 0})
            }break
    }
})
setInterval(() => {
    ctx.fillStyle = '#333333'
    ctx.fillRect(0, 0, canv.width, canv.height)
    ctx.fillStyle = 'green'
    ctx.fillRect(apple.x, apple.y, size, size)
    ctx.fillStyle = 'red'
    if (queue.length > 0){({dx, dy} = queue.pop())}
    snake.unshift({
        x: mod(snake[0].x+dx*size, canv.width - canv.width % size),
        y: mod(snake[0].y+dy*size, canv.height - canv.height % size)})
    dx_ = dx; dy_ = dy;
    if (snake[0].x === apple.x && snake[0].y === apple.y) {
        apple.x = Math.floor(Math.random() * div(canv.width, size)) * size
        apple.y = Math.floor(Math.random() * div(canv.height, size)) * size
    }
    else {snake.pop()}
    for (let i = 1; i < snake.length; i++) {
        if (snake[0].x === snake[i].x && snake[0].y === snake[i].y) {snake = [snake[i]]}
    }
    for (let j = 0; j < snake.length; j++) {
        ctx.fillRect(snake[j].x, snake[j].y, size, size)
    }
}, 30)