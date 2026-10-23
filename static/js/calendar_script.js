"use strict";

const dateTextEl = document.querySelector(".datetxt");
const dayTextEl = document.querySelector(".daytxt");
const datesEl = document.querySelector(".dates");
const monthYearEl = document.querySelector(".month_year");
const previousButton = document.querySelector("#prev");
const nextButton = document.querySelector("#next");
const timePickerEl = document.querySelector("#time-picker");
const timeSelectEl = document.querySelector("#reservation-time");
const bookButton = document.querySelector("#book-button");
const reservationForm = document.querySelector("#reservation-form");
const guestCountSelect = document.querySelector("#guest-count");
const phoneInput = document.querySelector("#phone");

const today = new Date();
let selectedDate = new Date(today.getFullYear(), today.getMonth(), today.getDate());
let displayedMonth = new Date(today.getFullYear(), today.getMonth(), 1);

function renderCalendar() {
    const year = displayedMonth.getFullYear();
    const month = displayedMonth.getMonth();
    const firstWeekday = (new Date(year, month, 1).getDay() + 6) % 7;
    const lastDate = new Date(year, month + 1, 0).getDate();
    const monthName = displayedMonth.toLocaleDateString("en", { month: "long" });

    monthYearEl.textContent = `${monthName}, ${year}`;
    dateTextEl.textContent = selectedDate.toLocaleDateString("en", {
        weekday: "short",
        day: "numeric",
        month: "short",
        year: "numeric"
    });
    dayTextEl.textContent = isToday(selectedDate) ? "Today" : "Selected";

    datesEl.replaceChildren();

    for (let blankDay = 0; blankDay < firstWeekday; blankDay += 1) {
        const blankDate = document.createElement("li");
        blankDate.className = "dummy";
        blankDate.setAttribute("aria-hidden", "true");
        datesEl.append(blankDate);
    }

    for (let day = 1; day <= lastDate; day += 1) {
        const date = document.createElement("li");
        date.textContent = day;
        date.tabIndex = 0;
        date.setAttribute("role", "button");

        if (
            selectedDate.getFullYear() === year &&
            selectedDate.getMonth() === month &&
            selectedDate.getDate() === day
        ) {
            date.classList.add("active");
            date.setAttribute("aria-pressed", "true");
        } else {
            date.setAttribute("aria-pressed", "false");
        }

        if (
            today.getFullYear() === year &&
            today.getMonth() === month &&
            today.getDate() === day
        ) {
            date.setAttribute("aria-current", "date");
        }

        datesEl.append(date);
    }
}

function isToday(date) {
    return (
        date.getFullYear() === today.getFullYear() &&
        date.getMonth() === today.getMonth() &&
        date.getDate() === today.getDate()
    );
}

function selectDate(dateElement) {
    const day = Number(dateElement.textContent);
    selectedDate = new Date(
        displayedMonth.getFullYear(),
        displayedMonth.getMonth(),
        day
    );
    renderTimeOptions(selectedDate);
    renderCalendar();
}

function renderTimeOptions(date) {
    const openingHour = date.getDay() === 0 || date.getDay() === 6 ? 13 : 16;
    const closingHour = 22;

    timeSelectEl.replaceChildren();
    bookButton.hidden = true;
    reservationForm.hidden = true;

    const placeholder = document.createElement("option");
    placeholder.value = "";
    placeholder.textContent = "Select a time";
    placeholder.disabled = true;
    placeholder.selected = true;
    timeSelectEl.append(placeholder);

    for (let hour = openingHour; hour < closingHour; hour += 1) {
        const option = document.createElement("option");
        option.value = `${String(hour).padStart(2, "0")}:00`;
        option.textContent = option.value;
        timeSelectEl.append(option);
    }

    timePickerEl.hidden = false;
}

timeSelectEl.addEventListener("change", () => {
    bookButton.hidden = !timeSelectEl.value;
    reservationForm.hidden = true;
});

phoneInput.addEventListener("input", () => {
    phoneInput.value = phoneInput.value.replace(/[^0-9+() .-]/g, "");
});

bookButton.addEventListener("click", () => {
    const selectedDateText = selectedDate.toLocaleDateString("en-GB", {
        day: "2-digit",
        month: "2-digit",
        year: "numeric"
    });
    const guests = guestCountSelect.value;

    document.querySelector("#summary-guests").textContent = guests;
    document.querySelector("#summary-date").textContent = selectedDateText;
    document.querySelector("#summary-time").textContent = timeSelectEl.value;
    document.querySelector("#booking-guests").value = guests;
    document.querySelector("#booking-date").value = [
        selectedDate.getFullYear(),
        String(selectedDate.getMonth() + 1).padStart(2, "0"),
        String(selectedDate.getDate()).padStart(2, "0")
    ].join("-");
    document.querySelector("#booking-time").value = timeSelectEl.value;

    reservationForm.hidden = false;
    reservationForm.scrollIntoView({ behavior: "smooth", block: "start" });
});

datesEl.addEventListener("click", (event) => {
    const dateElement = event.target.closest("li");
    if (dateElement && !dateElement.classList.contains("dummy")) {
        selectDate(dateElement);
    }
});

datesEl.addEventListener("keydown", (event) => {
    const dateElement = event.target.closest("li");
    if (
        dateElement &&
        !dateElement.classList.contains("dummy") &&
        (event.key === "Enter" || event.key === " ")
    ) {
        event.preventDefault();
        selectDate(dateElement);
    }
});

previousButton.addEventListener("click", () => {
    displayedMonth = new Date(
        displayedMonth.getFullYear(),
        displayedMonth.getMonth() - 1,
        1
    );
    renderCalendar();
});

nextButton.addEventListener("click", () => {
    displayedMonth = new Date(
        displayedMonth.getFullYear(),
        displayedMonth.getMonth() + 1,
        1
    );
    renderCalendar();
});

renderCalendar();
