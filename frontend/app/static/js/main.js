const url_root = 'http://raspberrypi5.local:5000';

document.addEventListener('DOMContentLoaded', function() {
    const img = document.querySelector('.video-frame img');
    const btn = document.getElementById('capture-btn');

    const plateEl = document.getElementById('plate');
    const checkInEl = document.getElementById('check-in-time');
    const checkOutEl = document.getElementById('check-out-time');
    const durationEl = document.getElementById('duration');
    const feeEl = document.getElementById('parking-fee');

    function formatDateTime(dateStr) {
        if (!dateStr || dateStr === '---') {
            return '---';
        }
        const date = new Date(dateStr);
        if (isNaN(date.getTime())) {
            return '---';
        }
        return date.toLocaleString('vi-VN');
    }

    function formatCurrency(amountStr) {
        if (!amountStr || amountStr === '---') {
            return '---';
        }
        const amount = parseFloat(amountStr);
        if (isNaN(amount)) {
            return '---';
        }
        return new Intl.NumberFormat('vi-VN', {
            style: 'currency',
            currency: 'VND'
        }).format(amount);
    }

    function updateUI(plateData) {
        plateEl.textContent = plateData.plate_text || '---';
        checkInEl.textContent = formatDateTime(plateData.check_in_time);
        checkOutEl.textContent = formatDateTime(plateData.check_out_time);
        durationEl.textContent = plateData.duration || '---';
        feeEl.textContent = formatCurrency(plateData.parking_fee);
    }

    btn.onclick = async () => {
        try {
            const canvas = document.createElement('canvas');
            canvas.width = img.naturalWidth || img.width;
            canvas.height = img.naturalHeight || img.height;
            const ctx = canvas.getContext('2d');
            ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
            const dataUrl = canvas.toDataURL('image/jpeg');

            const response = await fetch(url_root + '/capture', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({image: dataUrl})
            });

            const result = await response.json();

            if (result.available_spots !== undefined || result.occupied_spots !== undefined) {
                updateParkingDisplay(result.available_spots, result.occupied_spots);
            }

            if (result.status === 'success' && result.plates && result.plates.length > 0) {
                updateUI(result.plates[0]);
            } else {
                updateUI({
                    plate_text: 'Không nhận diện được',
                    check_in_time: '---',
                    check_out_time: '---',
                    duration: '---',
                    parking_fee: '---'
                });
            }
        } catch (error) {
            console.error('Lỗi:', error);
            alert('Có lỗi xảy ra khi xử lý ảnh!');
        }
    };
});

async function fetchParkingStatus() {
    try {
        const res = await fetch(url_root + '/api/parking-status');
        if (!res.ok) return;
        const data = await res.json();
        document.getElementById('available-spots').textContent = data.available_spots;
        document.getElementById('occupied-spots').textContent = data.occupied_spots;
    } catch (e) {
        console.error('Lỗi khi lấy trạng thái bãi:', e);
    }
}

function updateParkingDisplay(available, occupied) {
    if (available !== undefined) document.getElementById('available-spots').textContent = available;
    if (occupied !== undefined) document.getElementById('occupied-spots').textContent = occupied;
}

// Gọi khi DOM sẵn sàng
document.addEventListener('DOMContentLoaded', function() {
    fetchParkingStatus();
});