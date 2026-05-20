
document.addEventListener('DOMContentLoaded', function() {
    if (!requireAuth()) return;

    loadVisitors();
    loadVisitorStats();
    loadApartmentsForVisitor();

    // Visitor form submit handler
    const visitorForm = document.getElementById('visitorForm');
    if (visitorForm) {
        visitorForm.addEventListener('submit', handleVisitorSubmit);
    }
});

async function loadVisitors() {
    const token = localStorage.getItem('token');
    if (!token) {
        window.location.href = 'index.html';
        return;
    }

    try {
        const statusFilter = document.getElementById('filterStatus')?.value;
        const dateFilter = document.getElementById('filterDate')?.value;

        let url = API_BASE_URL + '/visitors';
        const params = [];
        if (statusFilter) params.push('status=' + statusFilter);
        if (dateFilter) params.push('date=' + dateFilter);
        if (params.length > 0) url += '?' + params.join('&');

        const response = await fetch(url, {
            headers: { 'Authorization': 'Bearer ' + token }
        });

        if (!response.ok) throw new Error('Failed to load visitors');

        const data = await response.json();
        renderVisitors(data.visitors);
    } catch (error) {
        console.error('Error loading visitors:', error);
        showAlert('Error loading visitors', 'danger');
    }
}

async function loadVisitorStats() {
    const token = localStorage.getItem('token');
    try {
        const response = await fetch(API_BASE_URL + '/visitors/current', {
            headers: { 'Authorization': 'Bearer ' + token }
        });
        const data = await response.json();
        const visitors = data.visitors || [];

        document.getElementById('currentInside').textContent = visitors.length;

        // Count today's visitors from the response
        const today = new Date().toISOString().split('T')[0];
        const todayCount = visitors.filter(v => v.entry_time && v.entry_time.startsWith(today)).length;
        document.getElementById('todayVisits').textContent = todayCount;
    } catch (error) {
        console.error('Error loading visitor stats:', error);
    }

    // Get total visitors
    try {
        const allResponse = await fetch(API_BASE_URL + '/visitors', {
            headers: { 'Authorization': 'Bearer ' + token }
        });
        const allData = await allResponse.json();
        document.getElementById('totalVisits').textContent = (allData.visitors || []).length;
    } catch (error) {
        console.error('Error loading total visitors:', error);
    }
}

function renderVisitors(visitors) {
    const tbody = document.getElementById('visitorsTable');
    if (!tbody) return;

    if (!visitors || visitors.length === 0) {
        tbody.innerHTML = '<tr><td colspan="9" class="text-center text-muted py-4">No visitors found</td></tr>';
        return;
    }

    tbody.innerHTML = visitors.map(v => `
        <tr>
            <td><strong>#${v.id}</strong></td>
            <td>${v.visitor_name}</td>
            <td>${v.phone || '-'}</td>
            <td><span class="badge bg-dark">${v.unit_number}</span></td>
            <td>${v.purpose}</td>
            <td>${formatDateTime(v.entry_time)}</td>
            <td>${v.exit_time ? formatDateTime(v.exit_time) : '<span class="text-muted">-</span>'}</td>
            <td><span class="badge ${getStatusBadgeClass(v.status)}">${v.status}</span></td>
            <td>
                ${v.status === 'inside' ? `
                <button class="btn btn-sm btn-success btn-action" onclick="logExit(${v.id})" title="Log Exit">
                    <i class="fas fa-sign-out-alt"></i>
                </button>
                ` : ''}
                <button class="btn btn-sm btn-info btn-action" onclick="viewVisitor(${v.id})" title="View">
                    <i class="fas fa-eye"></i>
                </button>
            </td>
        </tr>
    `).join('');
}

async function loadApartmentsForVisitor() {
    const token = localStorage.getItem('token');
    try {
        const response = await fetch(API_BASE_URL + '/apartments?status=occupied', {
            headers: { 'Authorization': 'Bearer ' + token }
        });
        const data = await response.json();
        const aptSelect = document.getElementById('visitorApartment');
        if (aptSelect) {
            aptSelect.innerHTML = '<option value="">Select Apartment</option>' +
                (data.apartments || []).map(a => `<option value="${a.id}">${a.unit_number}</option>`).join('');
        }
    } catch (error) {
        console.error('Error loading apartments:', error);
    }
}

async function handleVisitorSubmit(e) {
    e.preventDefault();

    const token = localStorage.getItem('token');

    const formData = {
        visitor_name: document.getElementById('visitorName').value,
        phone: document.getElementById('visitorPhone').value,
        email: document.getElementById('visitorEmail').value,
        apartment_id: parseInt(document.getElementById('visitorApartment').value),
        purpose: document.getElementById('visitorPurpose').value,
        visitor_count: parseInt(document.getElementById('visitorCount').value),
        notes: document.getElementById('visitorNotes').value
    };

    try {
        const response = await fetch(API_BASE_URL + '/visitors', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + token
            },
            body: JSON.stringify(formData)
        });

        if (response.ok) {
            bootstrap.Modal.getInstance(document.getElementById('visitorModal')).hide();
            document.getElementById('visitorForm').reset();
            loadVisitors();
            loadVisitorStats();
            showAlert('Visitor registered successfully!', 'success');
        } else {
            const data = await response.json();
            showAlert(data.error || 'Failed to register visitor', 'danger');
        }
    } catch (error) {
        showAlert('Error connecting to server', 'danger');
    }
}

async function logExit(visitorId) {
    if (!confirm('Log exit for this visitor?')) return;

    const token = localStorage.getItem('token');
    try {
        const response = await fetch(API_BASE_URL + '/visitors/' + visitorId + '/exit', {
            method: 'PUT',
            headers: { 'Authorization': 'Bearer ' + token }
        });

        if (response.ok) {
            loadVisitors();
            loadVisitorStats();
            showAlert('Visitor exit logged successfully!', 'success');
        } else {
            showAlert('Failed to log exit', 'danger');
        }
    } catch (error) {
        showAlert('Error logging exit', 'danger');
    }
}

async function viewVisitor(id) {
    showAlert('View visitor details for #' + id, 'info');
}
