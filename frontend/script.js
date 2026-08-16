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