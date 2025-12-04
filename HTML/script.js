let count = 0;

const countEl = document.getElementById("count");
const incBtn = document.getElementById("inc");
const decBtn = document.getElementById("dec");
const resetBtn = document.getElementById("reset");
const squareBtn = document.getElementById("square");


function render() {
  countEl.textContent = count;
}

incBtn.addEventListener("click", () => {
  count++;
  render();
});

decBtn.addEventListener("click", () => {
  count--;
  render();
});

resetBtn.addEventListener("click", () => {
    if(count > 0){
        count = 0;
        render();
    }
});

squareBtn.addEventListener("click", () => {
  count = count * count;
  render();
});

render();
