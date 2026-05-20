<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Smart Apartment - Visitors</title>
    <link
      href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css"
      rel="stylesheet"
    />
    <link
      href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css"
      rel="stylesheet"
    />
    <link href="css/styles.css" rel="stylesheet" />
  </head>
  <body>
    <nav class="sidebar" id="sidebar">
      <div class="sidebar-brand">
        <i class="fas fa-building"></i>
        Smart Apartment
      </div>
      <ul class="nav flex-column mt-3">
        <li class="nav-item">
          <a class="nav-link" href="dashboard.html">
            <i class="fas fa-home"></i>Dashboard
          </a>
        </li>
        <li class="nav-item">
          <a class="nav-link" href="apartments.html">
            <i class="fas fa-building"></i>Apartments
          </a>
        </li>
        <li class="nav-item admin-only">
          <a class="nav-link" href="users.html">
            <i class="fas fa-users"></i>Users
          </a>
        </li>
        <li class="nav-item">
          <a class="nav-link" href="bills.html">
            <i class="fas fa-file-invoice-dollar"></i>Bills
          </a>
        </li>
        <li class="nav-item security-only">
          <a class="nav-link active" href="visitors.html">
            <i class="fas fa-user-friends"></i>Visitors
          </a>
        </li>
        <li class="nav-item">
          <a class="nav-link" href="service-requests.html">
            <i class="fas fa-tools"></i>Service Requests
          </a>
        </li>
        <li class="nav-item mt-3">
          <a class="nav-link" href="#" id="logoutBtn">
            <i class="fas fa-sign-out-alt"></i>Logout
          </a>
        </li>
      </ul>
    </nav>

    <div class="main-content" id="mainContent">
      <nav class="top-navbar d-flex justify-content-between align-items-center">
        <div class="d-flex align-items-center">
          <button
            class="btn btn-link text-dark me-3 d-lg-none"
            id="sidebarToggle"
          >
            <i class="fas fa-bars fa-lg"></i>
          </button>
          <span class="navbar-brand mb-0 h4">Visitors</span>
        </div>
        <div class="d-flex align-items-center">
          <div class="user-info d-flex align-items-center">
            <div class="user-avatar me-2" id="userAvatar">A</div>
            <div>
              <div class="fw-semibold" id="userName">Admin</div>
              <small class="text-muted" id="userRole">Admin</small>
            </div>
          </div>
        </div>
      </nav>

      <div class="container-fluid p-4">
        <div
          class="page-header d-flex justify-content-between align-items-center"
        >
          <h4><i class="fas fa-user-friends me-2"></i>Visitor Management</h4>
          <button
            class="btn btn-primary"
            data-bs-toggle="modal"
            data-bs-target="#visitorModal"
          >
            <i class="fas fa-user-plus me-2"></i>Register Visitor
          </button>
        </div>

        <!-- Stats -->
        <div class="row g-4 mb-4">
          <div class="col-md-4">
            <div class="card stat-card">
              <div class="card-body">
                <div class="d-flex justify-content-between align-items-start">
                  <div>
                    <div class="stat-title">Current Inside</div>
                    <div class="stat-value text-info" id="currentInside">0</div>
                  </div>
                  <div class="stat-icon bg-info bg-opacity-10 text-info">
                    <i class="fas fa-users"></i>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div class="col-md-4">
            <div class="card stat-card">
              <div class="card-body">
                <div class="d-flex justify-content-between align-items-start">
                  <div>
                    <div class="stat-title">Total Visits Today</div>
                    <div class="stat-value" id="todayVisits">0</div>
                  </div>
                  <div class="stat-icon bg-primary bg-opacity-10 text-primary">
                    <i class="fas fa-calendar-day"></i>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div class="col-md-4">
            <div class="card stat-card">
              <div class="card-body">
                <div class="d-flex justify-content-between align-items-start">
                  <div>
                    <div class="stat-title">Total Visits</div>
                    <div class="stat-value" id="totalVisits">0</div>
                  </div>
                  <div
                    class="stat-icon bg-secondary bg-opacity-10 text-secondary"
                  >
                    <i class="fas fa-history"></i>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="filter-section">
          <div class="row g-3">
            <div class="col-md-4">
              <label class="form-label">Status</label>
              <select class="form-select" id="filterStatus">
                <option value="">All Status</option>
                <option value="inside">Inside</option>
                <option value="exited">Exited</option>
              </select>
            </div>
            <div class="col-md-4">
              <label class="form-label">Date</label>
              <input type="date" class="form-control" id="filterDate" />
            </div>
            <div class="col-md-4 d-flex align-items-end">
              <button class="btn btn-secondary w-100" onclick="loadVisitors()">
                <i class="fas fa-filter me-2"></i>Apply Filters
              </button>
            </div>
          </div>
        </div>

        <div class="table-container">
          <div class="table-responsive">
            <table class="table">
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Visitor Name</th>
                  <th>Phone</th>
                  <th>Apartment</th>
                  <th>Purpose</th>
                  <th>Entry Time</th>
                  <th>Exit Time</th>
                  <th>Status</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody id="visitorsTable">
                <tr>
                  <td colspan="9" class="text-center text-muted py-4">
                    Loading visitors...
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>

    <!-- Register Visitor Modal -->
    <div class="modal fade" id="visitorModal" tabindex="-1">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">
              <i class="fas fa-user-plus me-2"></i>Register Visitor
            </h5>
            <button
              type="button"
              class="btn-close"
              data-bs-dismiss="modal"
            ></button>
          </div>
          <form id="visitorForm">
            <div class="modal-body">
              <div class="row">
                <div class="col-md-6 mb-3">
                  <label class="form-label">Visitor Name</label>
                  <input
                    type="text"
                    class="form-control"
                    id="visitorName"
                    required
                  />
                </div>
                <div class="col-md-6 mb-3">
                  <label class="form-label">Phone</label>
                  <input type="tel" class="form-control" id="visitorPhone" />
                </div>
              </div>
              <div class="row">
                <div class="col-md-6 mb-3">
                  <label class="form-label">Email</label>
                  <input type="email" class="form-control" id="visitorEmail" />
                </div>
                <div class="col-md-6 mb-3">
                  <label class="form-label">Apartment to Visit</label>
                  <select class="form-select" id="visitorApartment" required>
                    <option value="">Select Apartment</option>
                  </select>
                </div>
              </div>
              <div class="row">
                <div class="col-md-6 mb-3">
                  <label class="form-label">Purpose of Visit</label>
                  <select class="form-select" id="visitorPurpose" required>
                    <option value="">Select Purpose</option>
                    <option value="Family Visit">Family Visit</option>
                    <option value="Friend Visit">Friend Visit</option>
                    <option value="Delivery">Delivery</option>
                    <option value="Maintenance">Maintenance</option>
                    <option value="Official">Official</option>
                    <option value="Other">Other</option>
                  </select>
                </div>
                <div class="col-md-6 mb-3">
                  <label class="form-label">Number of Visitors</label>
                  <input
                    type="number"
                    class="form-control"
                    id="visitorCount"
                    value="1"
                    min="1"
                  />
                </div>
              </div>
              <div class="mb-3">
                <label class="form-label">Notes</label>
                <textarea
                  class="form-control"
                  id="visitorNotes"
                  rows="2"
                ></textarea>
              </div>
            </div>
            <div class="modal-footer">
              <button
                type="button"
                class="btn btn-secondary"
                data-bs-dismiss="modal"
              >
                Cancel
              </button>
              <button type="submit" class="btn btn-primary">
                <i class="fas fa-user-check me-2"></i>Register Entry
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>
    <script src="js/app.js?v=3"></script>
    <script src="js/auth.js?v=3"></script>
    <script src="js/visitors.js"></script>
  </body>
</html>
