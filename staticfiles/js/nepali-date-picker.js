
class NepaliDatePicker {
    constructor() {
        // Nepali calendar data (2000-2089 BS)
        // Each array represents days in each month for that year
        this.nepaliCalendar = {
            2000: [30, 32, 31, 32, 31, 30, 30, 30, 29, 30, 29, 31],
            2001: [31, 31, 32, 31, 31, 31, 30, 29, 30, 29, 30, 30],
            2002: [31, 31, 32, 32, 31, 30, 30, 29, 30, 29, 30, 30],
            2003: [31, 32, 31, 32, 31, 30, 30, 30, 29, 29, 30, 31],
            2004: [30, 32, 31, 32, 31, 30, 30, 30, 29, 30, 29, 31],
            2005: [31, 31, 32, 31, 31, 31, 30, 29, 30, 29, 30, 30],
            2006: [31, 31, 32, 32, 31, 30, 30, 29, 30, 29, 30, 30],
            2007: [31, 32, 31, 32, 31, 30, 30, 30, 29, 29, 30, 31],
            2008: [31, 31, 31, 32, 31, 31, 29, 30, 30, 29, 29, 31],
            2009: [31, 31, 32, 31, 31, 31, 30, 29, 30, 29, 30, 30],
            2010: [31, 31, 32, 32, 31, 30, 30, 29, 30, 29, 30, 30],
            2011: [31, 32, 31, 32, 31, 30, 30, 30, 29, 29, 30, 31],
            2012: [31, 31, 31, 32, 31, 31, 29, 30, 30, 29, 30, 30],
            2013: [31, 31, 32, 31, 31, 31, 30, 29, 30, 29, 30, 30],
            2014: [31, 31, 32, 32, 31, 30, 30, 29, 30, 29, 30, 30],
            2015: [31, 32, 31, 32, 31, 30, 30, 30, 29, 29, 30, 31],
            2016: [31, 31, 31, 32, 31, 31, 29, 30, 30, 29, 30, 30],
            2017: [31, 31, 32, 31, 31, 31, 30, 29, 30, 29, 30, 30],
            2018: [31, 32, 31, 32, 31, 30, 30, 29, 30, 29, 30, 30],
            2019: [31, 32, 31, 32, 31, 30, 30, 30, 29, 30, 29, 31],
            2020: [31, 31, 31, 32, 31, 31, 30, 29, 30, 29, 30, 30],
            2021: [31, 31, 32, 31, 31, 31, 30, 29, 30, 29, 30, 30],
            2022: [31, 32, 31, 32, 31, 30, 30, 30, 29, 29, 30, 30],
            2023: [31, 32, 31, 32, 31, 30, 30, 30, 29, 30, 29, 31],
            2024: [31, 31, 31, 32, 31, 31, 30, 29, 30, 29, 30, 30],
            2025: [31, 31, 32, 31, 31, 31, 30, 29, 30, 29, 30, 30],
            2026: [31, 32, 31, 32, 31, 30, 30, 30, 29, 29, 30, 31],
            2027: [30, 32, 31, 32, 31, 30, 30, 30, 29, 30, 29, 31],
            2028: [31, 31, 32, 31, 31, 31, 30, 29, 30, 29, 30, 30],
            2029: [31, 31, 32, 31, 32, 30, 30, 29, 30, 29, 30, 30],
            2030: [31, 32, 31, 32, 31, 30, 30, 30, 29, 29, 30, 31],
            2031: [30, 32, 31, 32, 31, 30, 30, 30, 29, 30, 29, 31],
            2032: [31, 31, 32, 31, 31, 31, 30, 29, 30, 29, 30, 30],
            2033: [31, 31, 32, 32, 31, 30, 30, 29, 30, 29, 30, 30],
            2034: [31, 32, 31, 32, 31, 30, 30, 30, 29, 29, 30, 31],
            2035: [30, 32, 31, 32, 31, 31, 29, 30, 30, 29, 29, 31],
            2036: [31, 31, 32, 31, 31, 31, 30, 29, 30, 29, 30, 30],
            2037: [31, 31, 32, 32, 31, 30, 30, 29, 30, 29, 30, 30],
            2038: [31, 32, 31, 32, 31, 30, 30, 30, 29, 29, 30, 31],
            2039: [31, 31, 31, 32, 31, 31, 29, 30, 30, 29, 30, 30],
            2040: [31, 31, 32, 31, 31, 31, 30, 29, 30, 29, 30, 30],
            2041: [31, 31, 32, 32, 31, 30, 30, 29, 30, 29, 30, 30],
            2042: [31, 32, 31, 32, 31, 30, 30, 30, 29, 29, 30, 31],
            2043: [31, 31, 31, 32, 31, 31, 29, 30, 30, 29, 30, 30],
            2044: [31, 31, 32, 31, 31, 31, 30, 29, 30, 29, 30, 30],
            2045: [31, 32, 31, 32, 31, 30, 30, 29, 30, 29, 30, 30],
            2046: [31, 32, 31, 32, 31, 30, 30, 30, 29, 29, 30, 31],
            2047: [31, 31, 31, 32, 31, 31, 30, 29, 30, 29, 30, 30],
            2048: [31, 31, 32, 31, 31, 31, 30, 29, 30, 29, 30, 30],
            2049: [31, 32, 31, 32, 31, 30, 30, 30, 29, 29, 30, 30],
            2050: [31, 32, 31, 32, 31, 30, 30, 30, 29, 30, 29, 31],
            2051: [31, 31, 31, 32, 31, 31, 30, 29, 30, 29, 30, 30],
            2052: [31, 31, 32, 31, 31, 31, 30, 29, 30, 29, 30, 30],
            2053: [31, 32, 31, 32, 31, 30, 30, 30, 29, 29, 30, 30],
            2054: [31, 32, 31, 32, 31, 30, 30, 30, 29, 30, 29, 31],
            2055: [31, 31, 32, 31, 31, 31, 30, 29, 30, 29, 30, 30],
            2056: [31, 31, 32, 31, 32, 30, 30, 29, 30, 29, 30, 30],
            2057: [31, 32, 31, 32, 31, 30, 30, 30, 29, 29, 30, 31],
            2058: [30, 32, 31, 32, 31, 30, 30, 30, 29, 30, 29, 31],
            2059: [31, 31, 32, 31, 31, 31, 30, 29, 30, 29, 30, 30],
            2060: [31, 31, 32, 32, 31, 30, 30, 29, 30, 29, 30, 30],
            2061: [31, 32, 31, 32, 31, 30, 30, 30, 29, 29, 30, 31],
            2062: [30, 32, 31, 32, 31, 31, 29, 30, 29, 30, 29, 31],
            2063: [31, 31, 32, 31, 31, 31, 30, 29, 30, 29, 30, 30],
            2064: [31, 31, 32, 32, 31, 30, 30, 29, 30, 29, 30, 30],
            2065: [31, 32, 31, 32, 31, 30, 30, 30, 29, 29, 30, 31],
            2066: [31, 31, 31, 32, 31, 31, 29, 30, 30, 29, 29, 31],
            2067: [31, 31, 32, 31, 31, 31, 30, 29, 30, 29, 30, 30],
            2068: [31, 31, 32, 32, 31, 30, 30, 29, 30, 29, 30, 30],
            2069: [31, 32, 31, 32, 31, 30, 30, 30, 29, 29, 30, 31],
            2070: [31, 31, 32, 31, 31, 31, 30, 29, 30, 29, 30, 30],
            2071: [31, 31, 32, 31, 32, 30, 30, 29, 30, 29, 30, 30],
            2072: [31, 32, 31, 32, 31, 30, 30, 30, 29, 29, 30, 31],
            2073: [30, 32, 31, 32, 31, 30, 30, 30, 29, 30, 29, 31],
            2074: [31, 31, 32, 31, 31, 31, 30, 29, 30, 29, 30, 30],
            2075: [31, 31, 32, 32, 31, 30, 30, 29, 30, 29, 30, 30],
            2076: [31, 32, 31, 32, 31, 30, 30, 30, 29, 29, 30, 31],
            2077: [30, 32, 31, 32, 31, 31, 29, 30, 30, 29, 29, 31],
            2078: [31, 31, 32, 31, 31, 31, 30, 29, 30, 29, 30, 30],
            2079: [31, 31, 32, 32, 31, 30, 30, 29, 30, 29, 30, 30],
            2080: [31, 32, 31, 32, 31, 30, 30, 30, 29, 29, 30, 31],
            2081: [31, 31, 31, 32, 31, 31, 29, 30, 30, 29, 30, 30],
            2082: [31, 31, 32, 31, 31, 31, 30, 29, 30, 29, 30, 30],
            2083: [31, 31, 32, 32, 31, 30, 30, 29, 30, 29, 30, 30],
            2084: [31, 32, 31, 32, 31, 30, 30, 30, 29, 29, 30, 31],
            2085: [31, 31, 31, 32, 31, 31, 29, 30, 30, 29, 30, 30],
            2086: [31, 31, 32, 31, 31, 31, 30, 29, 30, 29, 30, 30],
            2087: [31, 32, 31, 32, 31, 30, 30, 29, 30, 29, 30, 30],
            2088: [31, 32, 31, 32, 31, 30, 30, 30, 29, 29, 30, 31],
            2089: [31, 31, 31, 32, 31, 31, 30, 29, 30, 29, 30, 30]
        };

        this.nepaliMonths = [
            'Baisakh', 'Jestha', 'Ashadh', 'Shrawan', 'Bhadra', 'Ashwin',
            'Kartik', 'Mangsir', 'Poush', 'Magh', 'Falgun', 'Chaitra'
        ];

        // Reference: 2000-01-01 BS = 1943-04-14 AD
        this.refDateAD = new Date('1943-04-14');
        this.refDateBS = { year: 2000, month: 1, day: 1 };
    }

    adToBs(adDate) {
        if (!adDate) return null;
        const delta = Math.floor((adDate - this.refDateAD) / (1000 * 60 * 60 * 24));
        let { year, month, day } = this.refDateBS;

        if (delta >= 0) {
            let remaining = delta;
            while (remaining > 0) {
                if (!this.nepaliCalendar[year]) return null;
                const daysInMonth = this.nepaliCalendar[year][month - 1];
                const daysRemaining = daysInMonth - day + 1;

                if (remaining >= daysRemaining) {
                    remaining -= daysRemaining;
                    day = 1;
                    month++;
                    if (month > 12) {
                        month = 1;
                        year++;
                    }
                } else {
                    day += remaining;
                    remaining = 0;
                }
            }
        } else {
            let remaining = Math.abs(delta);
            while (remaining > 0) {
                if (!this.nepaliCalendar[year]) return null;
                if (remaining >= day) {
                    remaining -= day;
                    month--;
                    if (month < 1) {
                        month = 12;
                        year--;
                        if (!this.nepaliCalendar[year]) return null;
                    }
                    day = this.nepaliCalendar[year][month - 1];
                } else {
                    day -= remaining;
                    remaining = 0;
                }
            }
        }
        return { year, month, day };
    }

    bsToAd(bsYear, bsMonth, bsDay) {
        if (!this.nepaliCalendar[bsYear]) return null;
        let totalDays = 0;
        const refBS = this.refDateBS;

        if (bsYear > refBS.year || (bsYear === refBS.year && bsMonth > refBS.month) ||
            (bsYear === refBS.year && bsMonth === refBS.month && bsDay >= refBS.day)) {
            for (let y = refBS.year; y < bsYear; y++) {
                if (!this.nepaliCalendar[y]) return null;
                totalDays += this.nepaliCalendar[y].reduce((a, b) => a + b, 0);
            }
            for (let m = 0; m < bsMonth - 1; m++) {
                totalDays += this.nepaliCalendar[bsYear][m];
            }
            totalDays += bsDay;
            for (let m = 0; m < refBS.month - 1; m++) {
                totalDays -= this.nepaliCalendar[refBS.year][m];
            }
            totalDays -= refBS.day;
        } else {
            for (let y = bsYear; y < refBS.year; y++) {
                if (!this.nepaliCalendar[y]) return null;
                totalDays -= this.nepaliCalendar[y].reduce((a, b) => a + b, 0);
            }
            for (let m = 0; m < refBS.month - 1; m++) {
                totalDays -= this.nepaliCalendar[refBS.year][m];
            }
            totalDays -= refBS.day;
            for (let m = 0; m < bsMonth - 1; m++) {
                totalDays += this.nepaliCalendar[bsYear][m];
            }
            totalDays += bsDay;
        }

        const resultDate = new Date(this.refDateAD);
        resultDate.setDate(resultDate.getDate() + totalDays);
        return resultDate;
    }

    formatDate(date) {
        if (!date) return '';
        const year = date.getFullYear();
        const month = String(date.getMonth() + 1).padStart(2, '0');
        const day = String(date.getDate()).padStart(2, '0');
        return `${year}-${month}-${day}`;
    }

    init(adInputId) {
        const adInput = document.getElementById(adInputId);
        if (!adInput) return;

        const container = adInput.parentElement;
        const nepaliContainer = document.createElement('div');
        nepaliContainer.className = 'nepali-date-input mt-2';
        nepaliContainer.innerHTML = `
            <div class="row g-2">
                <div class="col-4">
                    <input type="number" class="form-control form-control-sm nepali-year" 
                           placeholder="Year (BS)" min="2000" max="2089" id="${adInputId}_bs_year">
                </div>
                <div class="col-4">
                    <select class="form-select form-select-sm nepali-month" id="${adInputId}_bs_month">
                        <option value="">Month</option>
                        ${this.nepaliMonths.map((m, i) => `<option value="${i + 1}">${m}</option>`).join('')}
                    </select>
                </div>
                <div class="col-4">
                    <input type="number" class="form-control form-control-sm nepali-day" 
                           placeholder="Day" min="1" max="32" id="${adInputId}_bs_day">
                </div>
            </div>
            <small class="text-muted"><i class="bi bi-calendar2-check"></i> Nepali Date (BS): 2000-2089</small>
        `;

        container.appendChild(nepaliContainer);

        const bsYearInput = nepaliContainer.querySelector('.nepali-year');
        const bsMonthInput = nepaliContainer.querySelector('.nepali-month');
        const bsDayInput = nepaliContainer.querySelector('.nepali-day');

        adInput.addEventListener('change', () => {
            if (adInput.value) {
                const adDate = new Date(adInput.value);
                const bsDate = this.adToBs(adDate);
                if (bsDate) {
                    bsYearInput.value = bsDate.year;
                    bsMonthInput.value = bsDate.month;
                    bsDayInput.value = bsDate.day;
                }
            }
        });

        const updateAdFromBs = () => {
            const year = parseInt(bsYearInput.value);
            const month = parseInt(bsMonthInput.value);
            const day = parseInt(bsDayInput.value);
            if (year && month && day) {
                const adDate = this.bsToAd(year, month, day);
                if (adDate) {
                    adInput.value = this.formatDate(adDate);
                    adInput.dispatchEvent(new Event('change', { bubbles: true }));
                }
            }
        };

        bsYearInput.addEventListener('input', updateAdFromBs);
        bsMonthInput.addEventListener('change', updateAdFromBs);
        bsDayInput.addEventListener('input', updateAdFromBs);

        if (adInput.value) {
            const adDate = new Date(adInput.value);
            const bsDate = this.adToBs(adDate);
            if (bsDate) {
                bsYearInput.value = bsDate.year;
                bsMonthInput.value = bsDate.month;
                bsDayInput.value = bsDate.day;
            }
        }
    }
}

window.NepaliDatePicker = NepaliDatePicker;