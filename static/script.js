
console.log("scripts of html");
var stockSymbols = {};
async function getStockSymbols() {
    try {
        const response = await fetch('static\stockSymbols.json');
        const config = await response.json();
        stockSymbols =  config.stockSymbols;
    } catch (error) {
        console.error('Error fetching stock symbols:', error);
        stockSymbols = {}; // Return an empty array if there's an error
    }
}
getStockSymbols();

// Handle form submission
function handleQuestionSubmit(event) {
    event.preventDefault();  // Prevent form from reloading the page
    console.log("scripts of html handle");

    const userInput = document.getElementById('questionInput').value;
    const stockSymbols = ['TSLA', 'NVDA', 'THANGAMAYL'];
    
    if (userInput.trim() === '') {
        alert('Please enter a question.');
        return;
    }

    // Display loading indicator
    document.getElementById('generatedAnswer').innerHTML = 'Loading...';

    const foundSymbol = stockSymbols.find(symbol => userInput.includes(symbol));
    var requestData = {};
    if (foundSymbol) {
        requestData.question = userInput;
        requestData.symbol = foundSymbol; // Store found symbol directly
    } else {
        // Here you can implement additional logic to parse the input and find a symbol
        requestData.question = userInput;// Explicitly set to null if no symbol found
    }

    // Handle different types of questions dynamically
    if (userInput.toLowerCase().includes("compare stocks")) {
        const symbols = prompt("Enter stock symbols separated by commas (e.g., AAPL, GOOGL):");
        if (!symbols || symbols.trim() === '') {
            alert('Stock symbols are required for comparison.');
            document.getElementById('generatedAnswer').innerHTML = 'No symbols provided.';
            return;
        }
        requestData.symbols = symbols.trim();
    } else if (userInput.toLowerCase().includes("set alert")) {
        const stockSymbol = prompt("Enter the stock symbol (e.g., AAPL):");
        const targetPrice = prompt("Enter the target price (e.g., 150):");

        if (!stockSymbol || stockSymbol.trim() === '' || !targetPrice || isNaN(targetPrice)) {
            alert('Valid stock symbol and target price are required to set an alert.');
            document.getElementById('generatedAnswer').innerHTML = 'Invalid input for setting alert.';
            return;
        }
        requestData.stock_symbol = stockSymbol.trim();
        requestData.target_price = parseFloat(targetPrice);
    }

    // Make the fetch request to Flask API
    fetch('http://127.0.0.1:5000/ask-question', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestData)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        // Update output based on response data
        document.getElementById('generatedAnswer').innerHTML = data.generatedAnswer 
            ? `<strong>Generated Answer:</strong> ${data.generatedAnswer}`
            : '<strong>Generated Answer:</strong> No answer generated.';

        document.getElementById('actualAnswer').innerHTML = data.actualAnswer 
            ? `<strong>Actual Answer (from dataset):</strong> ${data.actualAnswer}`
            : '<strong>Actual Answer:</strong> No actual answer provided.';

        document.getElementById('context').innerHTML = data.context 
            ? `<strong>Context:</strong> ${data.context}`
            : '<strong>Context:</strong> No context provided.';
    })
    .catch(error => {
        console.error('Error:', error);
        document.getElementById('generatedAnswer').innerHTML = 'An error occurred. Please try again later.';
    });
}

// Handle the submission of the question
document.getElementById('questionForm').addEventListener('submit', handleQuestionSubmit);

// Exit button functionality
document.getElementById('exitBtn').addEventListener('click', function() {
    alert("Exiting the chatbot. Thank you!");
    window.close();  // This will only close the window if opened via script
});
