
const API_BASE_URL = 'http://raspberrypi5.local:5000/api';
const UPDATE_INTERVAL_MS = 30000; 
let occupancyChartInstance;
let dailyEntriesChartInstance;
let dailyRevenueChartInstance;
let monthlyRevenueChartInstance;



document.addEventListener('DOMContentLoaded', initializeDashboard);


function initializeDashboard() {
    Chart.defaults.color = 'rgba(224, 224, 224, 0.8)';
    Chart.defaults.font.family = "'Inter', sans-serif";
    
    loadDashboardData();
    
    setInterval(loadDashboardData, UPDATE_INTERVAL_MS); 
}



async function loadDashboardData() {
    console.log("Đang cập nhật dữ liệu dashboard...");
    
    const [
        statusData,
        revenueTodayData,
        dailyEntriesData,
        dailyRevenueData,
        monthlyRevenueData
    ] = await Promise.all([
        fetchData('/parking-status'),
        fetchData('/today-revenue'),
        fetchData('/daily-entries'),
        fetchData('/daily-revenue'),
        fetchData('/monthly-revenue')
    ]);


    if (statusData) {
        updateStatusCards(statusData);
        renderOccupancyChart(statusData);
    }
    if (revenueTodayData) {
        updateTodayRevenueCard(revenueTodayData);
    }
    if (dailyEntriesData) {
        renderDailyEntriesChart(dailyEntriesData);
    }
    if (dailyRevenueData) {
        renderDailyRevenueChart(dailyRevenueData);
    }
    if (monthlyRevenueData) {
        renderMonthlyRevenueChart(monthlyRevenueData);
    }
}



/**
 * Gửi yêu cầu fetch đến một endpoint của API và xử lý lỗi chung
 * @param {string} endpoint - Đường dẫn của API
 * @returns {Promise<object|null>} Dữ liệu JSON hoặc null nếu có lỗi
 */
async function fetchData(endpoint) {
    try {
        const response = await fetch(`${API_BASE_URL}${endpoint}`);
        if (!response.ok) {
            throw new Error(`Network response was not ok for ${endpoint} (status: ${response.status})`);
        }
        return await response.json();
    } catch (error) {
        console.error(`Lỗi khi lấy dữ liệu từ ${endpoint}:`, error);
        return null; 
    }
}

/**
 * Hàm trợ giúp chung để tạo hoặc cập nhật một biểu đồ.
 * Hủy biểu đồ cũ trước khi vẽ biểu đồ mới để tránh rò rỉ bộ nhớ.
 * @param {Chart} chartInstance - Biến chứa instance của biểu đồ hiện tại.
 * @param {string} canvasId - ID của thẻ canvas.
 * @param {object} chartConfig - Đối tượng cấu hình cho biểu đồ mới.
 * @returns {Chart} Instance của biểu đồ mới được tạo.
 */
function updateChart(chartInstance, canvasId, chartConfig) {
    const ctx = document.getElementById(canvasId).getContext('2d');
    if (chartInstance) {
        chartInstance.destroy();
    }
    return new Chart(ctx, chartConfig);
}



// Cập nhật các thẻ thông tin trạng thái bãi xe
function updateStatusCards(data) {
    document.getElementById('total-spots').innerText = data.total_spots;
    document.getElementById('occupied-spots').innerText = data.occupied_spots;
    document.getElementById('available-spots').innerText = data.available_spots;
}

// Cập nhật thẻ doanh thu trong ngày
function updateTodayRevenueCard(data) {
    document.getElementById('today-revenue').innerText = `${data.revenue.toLocaleString('vi-VN')} ₫`;
}

// Render biểu đồ tròn thể hiện tỉ lệ lấp đầy
function renderOccupancyChart(statusData) {
    const chartConfig = {
        type: 'pie',
        data: {
            labels: ['Chỗ trống', 'Đã có xe'],
            datasets: [{
                data: [statusData.available_spots, statusData.occupied_spots],
                backgroundColor: ['#50e3c2', '#4a90e2'],
                borderColor: '#2a2a4a',
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            plugins: { legend: { position: 'top' } }
        }
    };
    occupancyChartInstance = updateChart(occupancyChartInstance, 'occupancyChart', chartConfig);
}

// Render biểu đồ cột số lượt xe trong 7 ngày
function renderDailyEntriesChart(dailyData) {
    const chartConfig = {
        type: 'bar',
        data: {
            labels: dailyData.labels,
            datasets: [{
                label: 'Số lượt xe',
                data: dailyData.data,
                backgroundColor: 'rgba(74, 144, 226, 0.6)',
                borderColor: 'rgba(74, 144, 226, 1)',
                borderWidth: 1,
                borderRadius: 5
            }]
        },
        options: {
            responsive: true,
            plugins: { legend: { display: false } },
            scales: {
                y: { beginAtZero: true, grid: { color: 'rgba(224, 224, 224, 0.1)' } },
                x: { grid: { display: false } }
            }
        }
    };
    dailyEntriesChartInstance = updateChart(dailyEntriesChartInstance, 'dailyEntriesChart', chartConfig);
}
 
// Render biểu đồ đường doanh thu trong 7 ngày
function renderDailyRevenueChart(revenueData) {
    const chartConfig = {
        type: 'line',
        data: {
            labels: revenueData.labels,
            datasets: [{
                label: 'Doanh thu (VND)',
                data: revenueData.data,
                backgroundColor: 'rgba(80, 227, 194, 0.2)',
                borderColor: 'rgba(80, 227, 194, 1)',
                borderWidth: 2,
                fill: true,
                tension: 0.4
            }]
        },
        options: {
            responsive: true,
            plugins: { legend: { display: false } },
            scales: {
                y: {
                    beginAtZero: true,
                    grid: { color: 'rgba(224, 224, 224, 0.1)' },
                    ticks: { callback: value => `${(value / 1000).toLocaleString('vi-VN')}k` }
                },
                x: { grid: { display: false } }
            }
        }
    };
    dailyRevenueChartInstance = updateChart(dailyRevenueChartInstance, 'dailyRevenueChart', chartConfig);
}
 
// Render biểu đồ cột doanh thu theo tháng
function renderMonthlyRevenueChart(monthlyData) {
    const chartConfig = {
        type: 'bar',
        data: {
            labels: monthlyData.labels,
            datasets: [{
                label: 'Doanh thu (VND)',
                data: monthlyData.data,
                backgroundColor: 'rgba(74, 144, 226, 0.6)',
                borderColor: 'rgba(74, 144, 226, 1)',
                borderWidth: 1,
                borderRadius: 5
            }]
        },
        options: {
            responsive: true,
            plugins: { legend: { display: false } },
            scales: {
                y: {
                    beginAtZero: true,
                    grid: { color: 'rgba(224, 224, 224, 0.1)' },
                    ticks: { callback: value => `${(value / 1000000).toLocaleString('vi-VN')} Tr` }
                },
                x: { grid: { display: false } }
            }
        }
    };
    monthlyRevenueChartInstance = updateChart(monthlyRevenueChartInstance, 'monthlyRevenueChart', chartConfig);
}