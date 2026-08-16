async function loadDashboard() {
    try {
        // Get all customers
        const customerResponse = await fetch("/customers/");
        const customers = await customerResponse.json();

        // Get all jewelry items
        const jewelryResponse = await fetch("/jewelry/");
        const jewelry = await jewelryResponse.json();

        // Get all orders
        const orderResponse = await fetch("/orders/");
        const orders = await orderResponse.json();

        const completedOrders = orders.filter(
            order => order.status === "completed"
        );

        const totalSales = completedOrders.reduce(
            (total, order) => {
                const amount = parseFloat(
                    order.total_amount.replace("GHS ", "")
                );

                return total + amount;
            },
            0
        );

        // Display the counts
        document.getElementById("customer-count").textContent = customers.length;
        document.getElementById("jewelry-count").textContent = jewelry.length;
        document.getElementById("order-count").textContent = orders.length;

        document.getElementById("sales-total").textContent =
            `GHS ${totalSales.toFixed(2)}`;
        
        const customerTableBody = document.getElementById(
            "customer-table-body"
        );

        customerTableBody.innerHTML = "";

        customers.forEach(customer => {
            const row = document.createElement("tr");

            row.innerHTML = `
                <td>${customer.first_name}</td>
                <td>${customer.last_name}</td>
                <td>${customer.phone_number}</td>
                <td>${customer.email}</td>
                <td>${customer.address}</td>
                <td>
                    <button
                        class="action-button edit-button"
                        data-id="${customer.id}"
                    >
                        Edit
                    </button>
                    <button
                        class="action-button delete-button"
                        data-id="${customer.id}"
                    >
                        Delete
                    </button>
                </td>
            `;

            customerTableBody.appendChild(row);
        });

        const jewelryTableBody = document.getElementById(
            "jewelry-table-body"
        );

        jewelryTableBody.innerHTML = "";

        jewelry.forEach(item => {

            const row = document.createElement("tr");

            row.innerHTML = `
                <td>${item.name}</td>
                <td>${item.category}</td>
                <td>${item.material}</td>
                <td>${item.price}</td>
                <td>${item.stock_quantity}</td>

                <td>
                    <button
                        class="action-button jewelry-edit-button"
                        data-id="${item.id}"
                    >
                        Edit
                    </button>

                    <button
                        class="action-button jewelry-delete-button"
                        data-id="${item.id}"
                    >
                        Delete
                    </button>
                </td>
            `;

            jewelryTableBody.appendChild(row);
        });
        
        const orderTableBody = document.getElementById(
            "order-table-body"
        );

        orderTableBody.innerHTML = "";

        orders.forEach(order => {

            const customer = customers.find(
                customer => customer.id === order.customer_id
            );

            const customerName = customer
                ? `${customer.first_name} ${customer.last_name}`
                : "Unknown Customer";

            const row = document.createElement("tr");

            row.innerHTML = `
                <td>${customerName}</td>
                <td>${order.order_date}</td>
                <td>${order.status}</td>
                <td>${order.total_amount}</td>

                <td>
                    <button
                        class="action-button order-edit-button"
                        data-id="${order.id}"
                    >
                        Edit
                    </button>

                    <button
                        class="action-button order-delete-button"
                        data-id="${order.id}"
                    >
                        Delete
                    </button>
                </td>
            `;

            orderTableBody.appendChild(row);
        });

    } catch (error) {
        console.error("Error loading dashboard:", error);
    }
}

loadDashboard();

const customerForm = document.getElementById("customer-form");
const showCustomerFormButton = document.getElementById(
    "show-customer-form"
);
const cancelCustomerFormButton = document.getElementById(
    "cancel-customer-form"
);


// Show the customer form
showCustomerFormButton.addEventListener("click", () => {
    customerForm.classList.add("show");
});


// Hide the customer form
cancelCustomerFormButton.addEventListener("click", () => {
    customerForm.classList.remove("show");
    customerForm.reset();

    customerIdInput.value = "";

    customerSubmitButton.textContent = "Save Customer";
});


// Submit a new customer
customerForm.addEventListener("submit", async (event) => {

    event.preventDefault();

    const customerId = customerIdInput.value;

    const customerData = {
        first_name: document.getElementById("first-name").value,
        last_name: document.getElementById("last-name").value,
        phone_number: document.getElementById("phone-number").value,
        email: document.getElementById("email").value,
        address: document.getElementById("address").value
    };

    try {

        let response;

        if (customerId) {

            // Update existing customer
            response = await fetch(
                `/customers/${customerId}`,
                {
                    method: "PUT",

                    headers: {
                        "Content-Type": "application/json"
                    },

                    body: JSON.stringify(customerData)
                }
            );

        } else {

            // Create new customer
            response = await fetch(
                "/customers/",
                {
                    method: "POST",

                    headers: {
                        "Content-Type": "application/json"
                    },

                    body: JSON.stringify(customerData)
                }
            );
        }

        const result = await response.json();

        if (!response.ok) {
            alert(result.detail);
            return;
        }

        if (customerId) {
            alert("Customer updated successfully!");
        } else {
            alert("Customer created successfully!");
        }

        customerForm.reset();

        customerIdInput.value = "";

        customerSubmitButton.textContent = "Save Customer";

        customerForm.classList.remove("show");

        loadDashboard();

    } catch (error) {

        console.error("Error creating customer:", error);

        alert("Something went wrong while creating the customer.");
    }
});

const customerSubmitButton = document.getElementById(
    "customer-submit-button"
);

const customerIdInput = document.getElementById("customer-id");


// Handle Edit button clicks
document.addEventListener("click", async (event) => {

    if (!event.target.classList.contains("edit-button")) {
        return;
    }

    const customerId = event.target.dataset.id;

    try {

        const response = await fetch(
            `/customers/${customerId}`
        );

        const customer = await response.json();

        if (!response.ok) {
            alert(customer.detail);
            return;
        }

        customerIdInput.value = customer.id;

        document.getElementById("first-name").value =
            customer.first_name;

        document.getElementById("last-name").value =
            customer.last_name;

        document.getElementById("phone-number").value =
            customer.phone_number;

        document.getElementById("email").value =
            customer.email;

        document.getElementById("address").value =
            customer.address;

        customerSubmitButton.textContent = "Update Customer";

        customerForm.classList.add("show");

    } catch (error) {

        console.error("Error loading customer:", error);

        alert("Something went wrong while loading the customer.");
    }
});

document.addEventListener("click", async (event) => {

    if (!event.target.classList.contains("delete-button")) {
        return;
    }

    const customerId = event.target.dataset.id;

    const confirmed = confirm(
        "Are you sure you want to delete this customer?"
    );

    if (!confirmed) {
        return;
    }

    try {

        const response = await fetch(
            `/customers/${customerId}`,
            {
                method: "DELETE"
            }
        );

        const result = await response.json();

        if (!response.ok) {
            alert(result.detail);
            return;
        }

        alert("Customer deleted successfully!");

        loadDashboard();

    } catch (error) {

        console.error("Error deleting customer:", error);

        alert("Something went wrong while deleting the customer.");
    }
});

function showJewelryForm() {
    const form = document.getElementById("jewelry-form");

    if (form) {
        form.style.display = "block";
    }
}

function hideJewelryForm() {
    const form = document.getElementById("jewelry-form");

    if (form) {
        form.reset();
        form.style.display = "none";
    }
}


document.getElementById("jewelry-form").addEventListener(
    "submit",
    async function (event) {

        event.preventDefault();

        const jewelryId = document.getElementById(
            "jewelry-id"
        ).value;

        const jewelryData = {
            name: document.getElementById(
                "jewelry-name"
            ).value.trim(),

            category: document.getElementById(
                "jewelry-category"
            ).value,

            material: document.getElementById(
                "jewelry-material"
            ).value.trim(),

            price: parseFloat(
                document.getElementById(
                    "jewelry-price"
                ).value
            ),

            stock_quantity: parseInt(
                document.getElementById(
                    "jewelry-stock"
                ).value
            )
        };

        const url = jewelryId
            ? `/jewelry/${jewelryId}`
            : "/jewelry/";

        const method = jewelryId
            ? "PUT"
            : "POST";

        try {

            const response = await fetch(
                url,
                {
                    method: method,

                    headers: {
                        "Content-Type": "application/json"
                    },

                    body: JSON.stringify(jewelryData)
                }
            );

            const result = await response.json();

            if (!response.ok) {

                alert(
                    result.detail ||
                    "Failed to save jewelry item"
                );

                return;
            }

            alert(
                jewelryId
                    ? "Jewelry item updated successfully"
                    : "Jewelry item created successfully"
            );

            document.getElementById(
                "jewelry-form"
            ).reset();

            document.getElementById(
                "jewelry-id"
            ).value = "";

            document.getElementById(
                "jewelry-submit-button"
            ).textContent = "Save Jewelry";

            hideJewelryForm();

            loadDashboard();

        } catch (error) {

            console.error(
                "Error saving jewelry:",
                error
            );

            alert(
                "Something went wrong while saving the jewelry item."
            );
        }
    }
);

async function editJewelry(jewelryId) {
    try {
        const response = await fetch(`/jewelry/${jewelryId}`);

        const jewelry = await response.json();

        if (!response.ok) {
            alert(jewelry.detail || "Failed to get jewelry item");
            return;
        }

        document.getElementById("jewelry-id").value = jewelry.id;
        document.getElementById("jewelry-name").value = jewelry.name;
        document.getElementById("jewelry-category").value = jewelry.category;
        document.getElementById("jewelry-material").value = jewelry.material;
        document.getElementById("jewelry-price").value =
            parseFloat(jewelry.price.toString().replace("GHS", "").trim());
            
        document.getElementById("jewelry-stock").value = jewelry.stock_quantity;

        document.getElementById("jewelry-submit-button").textContent =
            "Update Jewelry";

        showJewelryForm();

    } catch (error) {
        console.error("Error getting jewelry item:", error);
        alert("Something went wrong while getting the jewelry item.");
    }
}

async function editOrder(orderId) {

    try {

        const response = await fetch(
            `/orders/${orderId}`
        );

        const order = await response.json();

        if (!response.ok) {

            alert(
                order.detail ||
                "Failed to get order"
            );

            return;
        }

        document.getElementById(
            "order-id"
        ).value = order.id;

        document.getElementById(
            "order-status"
        ).value = order.status;

        document.getElementById(
            "order-form"
        ).style.display = "block";

    } catch (error) {

        console.error(
            "Error getting order:",
            error
        );

        alert(
            "Something went wrong while getting the order."
        );
    }
}

async function deleteOrder(orderId) {

    const confirmed = confirm(
        "Are you sure you want to delete this order?"
    );

    if (!confirmed) {
        return;
    }

    try {

        const response = await fetch(
            `/orders/${orderId}`,
            {
                method: "DELETE"
            }
        );

        const result = await response.json();

        if (!response.ok) {

            alert(
                result.detail ||
                "Failed to delete order"
            );

            return;
        }

        alert("Order deleted successfully");

        loadDashboard();

    } catch (error) {

        console.error(
            "Error deleting order:",
            error
        );

        alert(
            "Something went wrong while deleting the order."
        );
    }
}

async function deleteJewelry(jewelryId) {

    const confirmed = confirm(
        "Are you sure you want to delete this jewelry item?"
    );

    if (!confirmed) {
        return;
    }

    try {

        const response = await fetch(
            `/jewelry/${jewelryId}`,
            {
                method: "DELETE"
            }
        );

        const result = await response.json();

        if (!response.ok) {

            alert(
                result.detail ||
                "Failed to delete jewelry item"
            );

            return;
        }

        alert("Jewelry item deleted successfully");

        loadDashboard();

    } catch (error) {

        console.error(
            "Error deleting jewelry:",
            error
        );

        alert(
            "Something went wrong while deleting the jewelry item."
        );
    }
}

document.addEventListener("click", function (event) {

    if (event.target.classList.contains("jewelry-edit-button")) {

        const jewelryId = event.target.dataset.id;

        editJewelry(jewelryId);
    }

});

document.addEventListener("click", function (event) {

    if (
        event.target.classList.contains(
            "jewelry-delete-button"
        )
    ) {

        const jewelryId = event.target.dataset.id;

        deleteJewelry(jewelryId);
    }

});
document.addEventListener("click", function (event) {

    if (
        event.target.classList.contains(
            "order-edit-button"
        )
    ) {

        const orderId =
            event.target.dataset.id;

        editOrder(orderId);
    }

});

document.addEventListener("click", function (event) {

    if (
        event.target.classList.contains(
            "order-delete-button"
        )
    ) {

        const orderId =
            event.target.dataset.id;

        deleteOrder(orderId);
    }

});

document.getElementById("order-form").addEventListener(
    "submit",
    async function (event) {

        event.preventDefault();

        const orderId = document.getElementById(
            "order-id"
        ).value;

        const status = document.getElementById(
            "order-status"
        ).value;

        try {

            const response = await fetch(
                `/orders/${orderId}`,
                {
                    method: "PUT",

                    headers: {
                        "Content-Type": "application/json"
                    },

                    body: JSON.stringify({
                        status: status
                    })
                }
            );

            const result = await response.json();

            if (!response.ok) {

                alert(
                    result.detail ||
                    "Failed to update order"
                );

                return;
            }

            alert(
                "Order updated successfully"
            );

            document.getElementById(
                "order-form"
            ).reset();

            document.getElementById(
                "order-id"
            ).value = "";

            document.getElementById(
                "order-form"
            ).style.display = "none";

            loadDashboard();

        } catch (error) {

            console.error(
                "Error updating order:",
                error
            );

            alert(
                "Something went wrong while updating the order."
            );
        }
    }
);
document.getElementById("cancel-order-form").addEventListener(
    "click",
    function () {

        const orderForm = document.getElementById(
            "order-form"
        );

        orderForm.reset();

        document.getElementById(
            "order-id"
        ).value = "";

        orderForm.style.display = "none";
    }
);
