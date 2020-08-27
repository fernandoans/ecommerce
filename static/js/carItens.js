function updateProduto(produtoId, acao) {
    var url = '/upd-item/'
    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({ 'produtoId': produtoId, 'acao': acao })
    }).then((response) => {
        return response.json();
    }).then((data) => {
        location.reload()
    });
}

function addItem(produtoId) {
    var url = '/add-item/'
    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({ 'produtoId': produtoId })
    }).then((response) => {
        return response.json();
    }).then((data) => {
        location.reload()
    });
}