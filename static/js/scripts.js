document.addEventListener('DOMContentLoaded', async () => {
    const cartCount = document.getElementById('cart-count');
    const cartCountLink = document.getElementById('cart-count-link');
    let cartItems = JSON.parse(localStorage.getItem('cartItems')) || [];

    const updateCartCount = () => {
        cartCount.textContent = cartItems.length;
        cartCountLink.textContent = `(${cartItems.length})`;
    };

    const fetchPizzas = async () => {
        try {
            const response = await fetch('/api/pizzas');
            if (!response.ok) throw new Error('Network response was not ok');
            const pizzas = await response.json();
            const pizzaMenu = document.getElementById('pizza-menu');

            pizzas.forEach(pizza => {
                const pizzaCard = `
                    <div class="col-md-3">
                        <div class="card mb-4">
                            <img src="${pizza.image}" class="card-img-top" alt="${pizza.flavor}">
                            <div class="card-body">
                                <h5 class="card-title">${pizza.flavor}</h5>
                                <button class="btn btn-primary add-to-cart" data-flavor="${pizza.flavor}">Add to Cart</button>
                            </div>
                        </div>
                    </div>`;
                pizzaMenu.innerHTML += pizzaCard;
            });
            attachAddToCartEvent();
        } catch (error) {
            console.error('Error fetching pizzas:', error);
        }
    };

    const removeCartItem = async index => {
        const item = cartItems[index];
        const response = await fetch(`/api/orders/${item._id}`, {
            method: 'DELETE',
        });
        if (response.ok) {
            cartItems.splice(index, 1);
            localStorage.setItem('cartItems', JSON.stringify(cartItems));
            updateCartCount();
            renderCart();
            alert('Item removed from cart.');
        } else {
            alert('Error removing item from cart.');
        }
    };

    const updateCartItem = async index => {
        const crust = prompt('Choose new crust: Thin, Thick, Stuffed', cartItems[index].crust);
        const size = prompt('Choose new size: Small, Medium, Large', cartItems[index].size);
        if (crust && size) {
            cartItems[index].crust = crust;
            cartItems[index].size = size;
            const item = cartItems[index];
            const response = await fetch(`/api/orders/${item._id}`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ crust, size, flavor: item.flavor }),
            });
            if (response.ok) {
                const updatedItem = await response.json();
                cartItems[index] = updatedItem;
                localStorage.setItem('cartItems', JSON.stringify(cartItems));
                updateCartCount();
                renderCart();
                alert('Item updated.');
            } else {
                alert('Error updating item.');
            }
        } else {
            alert('You must choose both crust and size.');
        }
    };

    const renderCartItems = () => {
        let cartHtml = '<ul>';
        cartItems.forEach((item, index) => {
            cartHtml += `
                <li>
                    ${item.flavor} - ${item.crust} crust - ${item.size} size 
                    <button class="btn btn-danger btn-sm" onclick="removeCartItem(${index})">Remove</button>
                    <button class="btn btn-secondary btn-sm" onclick="updateCartItem(${index})">Update</button>
                </li>`;
        });
        cartHtml += '</ul>';
        return cartHtml;
    };

    const renderCart = () => {
        const cartWindow = window.open('', 'Cart', 'width=600,height=400');
        cartWindow.removeCartItem = removeCartItem;
        cartWindow.updateCartItem = updateCartItem;

        cartWindow.document.open();
        cartWindow.document.write(`
            <html>
            <head>
                <title>Cart</title>
                <link rel="stylesheet" type="text/css" href="/static/css/cart.css">
            </head>
            <body>
                <h1>Your Cart</h1>
                ${renderCartItems()}
                <div id="cart-status">${cartItems.length === 0 ? 'Your cart is empty.' : ''}</div>
            </body>
            </html>
        `);
        cartWindow.document.close();
    };

    const attachAddToCartEvent = () => {
        const addToCartButtons = document.querySelectorAll('.add-to-cart');
        addToCartButtons.forEach(button => {
            button.addEventListener('click', async event => {
                const flavor = event.target.getAttribute('data-flavor');
                const crust = prompt('Choose crust: Thin, Thick, Stuffed');
                const size = prompt('Choose size: Small, Medium, Large');

                if (crust && size) {
                    const user_id = sessionStorage.getItem('user_id');

                    const response = await fetch('/api/orders', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({
                            flavor,
                            crust,
                            size,
                            user_id: user_id || null,
                        }),
                    });

                    if (response.ok) {
                        const cartItem = await response.json();
                        cartItems.push(cartItem);
                        localStorage.setItem('cartItems', JSON.stringify(cartItems));
                        updateCartCount();
                        alert(`${flavor} pizza with ${crust} crust and ${size} size added to cart.`);
                    } else {
                        alert('Error adding item to cart.');
                    }
                } else {
                    alert('You must choose both crust and size.');
                }
            });
        });
    };

    updateCartCount();
    await fetchPizzas();

    const ordersLink = document.getElementById('orders-link');
    if (ordersLink) {
        ordersLink.addEventListener('click', event => {
            event.preventDefault();
            renderCart();
        });
    }
});
