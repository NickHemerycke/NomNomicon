const listContainer1 = document.getElementById('appetizer-list');
const listContainer2 = document.getElementById('lunches-list');
const listContainer3 = document.getElementById('dinners-list');
const input1 = document.getElementById('item-input1');
const input2 = document.getElementById('item-input2');
const input3 = document.getElementById('item-input3');

function addItemApp() {
    const value = input1.value.trim();
    if (value) {
        const div = document.createElement('div');
        div.textContent = value;

        const removeBtn = document.createElement('button');
        removeBtn.textContent = 'Remove';
        removeBtn.onclick = () => div.remove();

        div.appendChild(removeBtn);
        listContainer1.appendChild(div);

        input1.value = '';
    }
}

function addItemLunch() {
    const value = input2.value.trim();
    if (value) {
        const div = document.createElement('div');
        div.textContent = value;

        const removeBtn = document.createElement('button');
        removeBtn.textContent = 'Remove';
        removeBtn.onclick = () => div.remove();

        div.appendChild(removeBtn);
        listContainer2.appendChild(div);

        input2.value = '';
    }
}

function addItemDinner() {
    const value = input3.value.trim();
    if (value) {
        const div = document.createElement('div');
        div.textContent = value;

        const removeBtn = document.createElement('button');
        removeBtn.textContent = 'Remove';
        removeBtn.onclick = () => div.remove();

        div.appendChild(removeBtn);
        listContainer3.appendChild(div);

        input3.value = '';
    }
}
