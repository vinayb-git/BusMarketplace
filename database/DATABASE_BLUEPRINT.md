# Bus Marketplace Database Blueprint

## 1. Purpose

This document defines the database architecture for the Bus Marketplace platform.

Goals:

- Highly normalized
- Scalable
- Maintainable
- High performance
- Easy auditing
- Support future growth
- Support multiple operators
- Support millions of bookings

---

# 2. Database Principles

The platform must:

- Never duplicate master data unnecessarily.
- Keep transactional and master data separate.
- Store complete audit history.
- Support soft deletion where appropriate.
- Use UUIDs for public-facing identifiers where appropriate.
- Maintain referential integrity through foreign keys.
- Optimize read-heavy search operations.
- Support partitioning for large transactional tables.

---

# 3. Database Modules

The database is divided into the following domains.

## Identity

Purpose:
Manage authentication and authorization.

Examples:

- Users
- Roles
- Permissions
- Sessions
- OTP
- Login history

Estimated Tables:
12

---

## Operator

Purpose:

Manage operator information.

Examples:

- Operator
- Branch
- Documents
- Bank Accounts
- Contacts
- Staff

Estimated Tables:
18

---

## Bus Management

Purpose:

Manage buses and coach configurations.

Examples:

- Bus
- Coach Type
- Amenities
- Bus Images
- Insurance
- Permits

Estimated Tables:
18

---

## Seat Layout Engine

Purpose:

Render any supported coach layout.

Examples:

- Layout Template
- Layout Sections
- Seats
- Seat Coordinates
- Seat Types
- Seat Groups
- Layout Versions

Estimated Tables:
18

---

## Location Engine

Purpose:

Maintain standardized locations.

Examples:

- Country
- State
- District
- City
- Boarding Point
- Drop Point
- Location Alias
- Geo Coordinates

Estimated Tables:
24

---

## Route Engine

Purpose:

Store reusable routes.

Examples:

- Route
- Route Stops
- Stop Timings
- Pickup Points
- Drop Points

Estimated Tables:
15

---

## Trip Engine

Purpose:

Manage scheduled trips.

Examples:

- Trip
- Trip Schedule
- Assigned Bus
- Assigned Driver

Estimated Tables:
15

---

## Inventory Engine

Purpose:

Manage seat ownership and availability.

Examples:

- Trip Seats
- Segment Availability
- Marketplace Allocation
- Seat Hold
- Inventory Audit

Estimated Tables:
30

---

## Booking Engine

Purpose:

Handle customer reservations.

Examples:

- Booking
- Passenger
- Booking Seats
- Tickets
- Boarding Pass

Estimated Tables:
20

---

## Payment Engine

Purpose:

Payment processing.

Examples:

- Payment
- Transaction
- Refund
- Settlement

Estimated Tables:
18

---

## Tracking Engine

Purpose:

Track buses.

Examples:

- GPS Devices
- Driver Location
- Trip Tracking
- ETA History

Estimated Tables:
12

---

## Notification Engine

Purpose:

Send notifications.

Examples:

- Templates
- SMS
- Email
- Push
- WhatsApp

Estimated Tables:
12

---

## Review Engine

Purpose:

Ratings and reviews.

Estimated Tables:
6

---

## Audit Engine

Purpose:

Track every important change.

Estimated Tables:
18

---

## Reporting

Purpose:

Reporting and analytics.

Examples:

- Daily Revenue
- Operator Statistics
- Booking Summary

Estimated Tables:
15

---

# 4. Estimated Database Size

| Module | Tables |
|---------|-------:|
| Identity | 12 |
| Operator | 18 |
| Bus | 18 |
| Seat Layout | 18 |
| Location | 24 |
| Route | 15 |
| Trips | 15 |
| Inventory | 30 |
| Booking | 20 |
| Payment | 18 |
| Tracking | 12 |
| Notifications | 12 |
| Reviews | 6 |
| Audit | 18 |
| Reporting | 15 |

Estimated Total:

Approximately **250 tables**

---

# 5. Core Design Engines

The platform is built around five reusable engines.

## Location Engine

Responsibilities:

- Standardized locations
- Canonical names
- Search aliases
- Geo coordinates
- Boarding points

---

## Seat Layout Engine

Responsibilities:

- Render any coach layout
- Lower and upper sections
- Seat coordinates
- Seat properties
- Layout templates

---

## Route Engine

Responsibilities:

- Route creation
- Stop ordering
- Timings
- Pickup and drop points
- Intermediate searches

---

## Inventory Engine

Responsibilities:

- Seat ownership
- Marketplace allocations
- Segment availability
- Seat locking
- Exclusive pricing

---

## Pricing Engine

Responsibilities:

- Operator pricing
- Marketplace pricing
- Bid matching
- Promotions
- Future dynamic pricing

---

# 6. Database Standards

Every table should contain where applicable:

- Primary Key
- Created Date
- Updated Date
- Created By
- Updated By
- Status
- Active Flag
- Version Number

Large transactional tables should also include:

- Audit Reference
- Tenant (Operator)
- Partition Key

