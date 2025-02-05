function debounce(func, delay) {
    let timer;
    return function (...args) {
        clearTimeout(timer);
        timer = setTimeout(() => func.apply(this, args), delay);
    };
}

function handleInput(inputId, dropdownId, type) {
    const input = document.getElementById(inputId);
    const dropdown = document.getElementById(dropdownId);
    console.log(`Initializing: ${inputId}, Dropdown:`, dropdown); // ✅ Debug log
    console.log("Dropdown Element:", dropdown);

    if (!input || !dropdown) {
        console.error(`ERROR: Input or dropdown not found: ${inputId}, ${dropdownId}`);
        return;
    }
    let activeIndex = -1;

    document.addEventListener('click', (e) => {
        if (!input.contains(e.target) && !dropdown.contains(e.target)) {
            dropdown.innerHTML = '';
            dropdown.style.display = 'none'; 
        }
    });

    const debouncedSearch = debounce(async function () {
        const query = input.value.trim();
        if (query.length > 0) {
            try {
                const response = await fetch(`/autocomplete/${type}?query=${encodeURIComponent(query)}`);
                const data = await response.json();
                console.log("API Response Data:", data);
                displayResults(data);
            } catch (error) {
                console.error("Error fetching search results:", error);
            }
        } else {
            dropdown.innerHTML = '';
            dropdown.style.display = 'none';
        }
    }, 300); // Debounce delay: 300ms

    input.addEventListener('input', debouncedSearch);

    input.addEventListener('focus', () => {
        if (input.value.trim().length > 0) {
            debouncedSearch();
        }
    });

    function displayResults(results,) {
        console.log("Dropdown Element:", dropdown);  // ✅ Debugging log
        dropdown.innerHTML = '';
    
        if (results.length === 0) {
            dropdown.style.display = 'none';
            return;
        }
    
        dropdown.style.display = 'block';
        dropdown.style.width = input.offsetWidth + 'px';
    
        results.forEach((item) => {
            console.log("Dropdown Item Data:", item);  // ✅ Debugging log
            const div = document.createElement('div');
            div.classList.add('autocomplete-item');
            div.textContent = item.display;  // ✅ Ensure correct field
            div.addEventListener('click', () => {
                input.value = item.display;
                const hiddenInput = document.getElementById(input.id + '-icao');
                if (hiddenInput) {
                    hiddenInput.value = item.IATA || "";
                }
                dropdown.innerHTML = '';
            });
            dropdown.appendChild(div);
        });
    }
    

    input.addEventListener('keydown', function (e) {
        const items = dropdown.getElementsByClassName('autocomplete-item');

        if (e.key === 'ArrowDown') {
            activeIndex = (activeIndex + 1) % items.length;
            updateActiveItem(items);
        } else if (e.key === 'ArrowUp') {
            activeIndex = (activeIndex - 1 + items.length) % items.length;
            updateActiveItem(items);
        } else if (e.key === 'Enter' && activeIndex > -1) {
            items[activeIndex].click();
            e.preventDefault();
        }
    });

    function updateActiveItem(items) {
        for (let item of items) {
            item.classList.remove('active');
        }
        if (items[activeIndex]) {
            items[activeIndex].classList.add('active');
        }
    }
}

document.addEventListener('DOMContentLoaded', () => {
    // Call handleInput for each field that needs autocomplete
    handleInput('origin', 'origin-dropdown', 'airports');
    handleInput('destination', 'destination-dropdown', 'airports');
    // NEW: call handleInput for airline
    handleInput('airline', 'airline-dropdown', 'airlines');
});


