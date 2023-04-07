let canv = document.createElement('canvas');
canv.height = document.documentElement.clientHeight
canv.width = document.documentElement.clientWidth

document.getElementsByTagName("body")[0].appendChild(canv);

const ctx = canv.getContext('2d')

ctx.clearRect(0,0, canv.width, canv.height)

function addMove(dir) {
    switch (dir) {
        case 'up':
            if ((queue.length > 0 ? queue[0].dy : dy) === 0) {
                    queue.unshift({dx: 0, dy: -1})
                // if (queue.length > 5) {queue.pop()}
            }break
        case 'down':
            if ((queue.length > 0 ? queue[0].dy : dy) === 0) {
                queue.unshift({dx: 0, dy: 1})
                // if (queue.length > 5) {queue.pop()}
            }break
        case 'left':
            if ((queue.length > 0 ? queue[0].dx : dx) === 0) {
                queue.unshift({dx: -1, dy: 0})
                // if (queue.length > 5) {queue.pop()}
            }break
        case 'right':
            if ((queue.length > 0 ? queue[0].dx : dx) === 0) {
                queue.unshift({dx: 1, dy: 0})
                // if (queue.length > 5) {queue.pop()}
            }break
    }
}

const mod = (a, b) => (b + (a % b)) % b
const div = (a, b) => ((a / b) | 0)
const prop = canv.height / canv.width
let delay = 100

const size = 20
let snake = [{x: 0, y: 0}]
let apple = {x: 100, y: 100}
let queue = [{dx: 1, dy: 0}]
let dx = 1, dy = 0
// alert('кто прочитал тот лох')

document.addEventListener('touchstart', ev => {
    if (ev.touches[ev.touches.length-1].clientY<=ev.touches[ev.touches.length-1].clientX*prop) {
        if (ev.touches[ev.touches.length-1].clientY<=(canv.width - ev.touches[ev.touches.length-1].clientX)*prop) {
            addMove('up')
        }
        else {
            addMove('right')
        }
    } else {
        if (ev.touches[ev.touches.length-1].clientY<=(canv.width - ev.touches[ev.touches.length-1].clientX)*prop) {
            addMove('left')
        }
        else {
            addMove('down')
        }
    }
})
document.addEventListener('keydown', (ev) => {if (ev.keyCode === 16) {delay = 30}})
document.addEventListener('keyup', (ev) => {if (ev.keyCode === 16) {delay = 100}})
document.addEventListener('keydown' ,ev => {if (ev.keyCode === 32) {apple.x = snake[0].x +dx*size; apple.y = snake[0].y+dy*size;}})
document.addEventListener('keydown', ev =>{
    switch (ev.keyCode) {
        case 38: addMove('up')
            break
        case 40: addMove('down')
            break
        case 37: addMove('left')
            break
        case 39: addMove('right')
            break
    }
})

function gameLoop() {
    requestAnimationFrame(gameLoop)
    let curTime = new Date().getTime()
    if (curTime - startTime > delay) {
        startTime = curTime
        ctx.clearRect(0, 0, canv.width, canv.height)
        ctx.fillStyle = '#ff0056'
        ctx.fillRect(apple.x, apple.y, size, size)
        ctx.fillStyle = '#1FBF66'

        if (queue.length > 0) {
            ({dx, dy} = queue.pop())
        }
        snake.unshift({
            x: mod(snake[0].x + dx * size, canv.width - canv.width % size),
            y: mod(snake[0].y + dy * size, canv.height - canv.height % size)
        })

        if (snake[0].x === apple.x && snake[0].y === apple.y) {  // Eat and respawn apple
            apple.x = Math.floor(Math.random() * div(canv.width, size)) * size
            apple.y = Math.floor(Math.random() * div(canv.height, size)) * size
        } else {
            snake.pop()
        }
        for (let i = 1; i < snake.length; i++) {  // Death check
            if (snake[0].x === snake[i].x && snake[0].y === snake[i].y) {
                snake = [snake[i]]
            }
        }
        for (let i = 0; i < snake.length; i++) {  // Draw snake
            if (i % 6 >= 3){ctx.fillStyle = '#7FE881'}
            else {ctx.fillStyle = '#1FBF66'}
            ctx.fillRect(snake[i].x, snake[i].y, size, size)
        }
    }
}
let startTime = new Date().getTime()
gameLoop()
