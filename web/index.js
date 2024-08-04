async function getDataFromPython() {
    document.getElementById('myele').innerText = await eel.get_data()();
    
}

document.getElementById('mybtn').addEventListener('click', () => {
    getDataFromPython();
})