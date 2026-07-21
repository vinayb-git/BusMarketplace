# Bus Marketplace Entity Relationship Model

## Purpose

This document identifies every major business entity in the Bus Marketplace platform and describes how each entity relates to others.

This document is the foundation for:

- Database schema
- REST APIs
- Microservices
- UI design
- Reporting
- Testing

---

# Level 1 Architecture

Platform

├── Identity
├── Operator
├── Bus
├── Seat Layout
├── Location
├── Route
├── Trip
├── Inventory
├── Booking
├── Payment
├── Tracking
├── Notification
├── Review
├── Settlement
└── Administration

---

# Identity Module

User
│
├── User Roles
├── Permissions
├── Sessions
├── Login History
├── OTP
└── Devices

Relationship

User (1)
↓

Many Sessions

User (1)

↓

Many Roles

---

# Operator Module

Operator

│

├── Branches

├── Staff

├── Bank Accounts

├── Documents

├── Buses

├── Drivers

└── Routes

Relationships

Operator (1)

↓

Many Buses

Operator (1)

↓

Many Routes

Operator (1)

↓

Many Staff

---

# Bus Module

Bus

│

├── Coach Type

├── Amenities

├── Images

├── Insurance

├── Permit

└── Layout Template

Relationship

Bus (1)

↓

One Layout Template

Bus (1)

↓

Many Trips

---

# Seat Layout Engine

Layout Template

│

├── Sections

├── Seats

├── Seat Types

├── Coordinates

└── Layout Version

Relationship

Layout (1)

↓

Many Sections

Section (1)

↓

Many Seats

Seat

↓

Adjacent Seat

---

# Location Engine

Country

↓

State

↓

District

↓

City

↓

Boarding Point

↓

Pickup Point

Relationships

State

↓

Many Districts

District

↓

Many Cities

City

↓

Many Boarding Points

Boarding Point

↓

Many Pickup Schedules

---

# Route Engine

Route

↓

Route Stops

↓

Pickup Points

↓

Drop Points

↓

Timings

Relationship

Route

↓

Many Stops

Each Stop

↓

Many Pickup Points

Each Stop

↓

Many Drop Points

---

# Trip Engine

Trip

↓

Bus

↓

Driver

↓

Trip Seats

↓

Tracking

Relationship

Route

↓

Many Trips

Trip

↓

Many Seats

Trip

↓

One Bus

---

# Inventory Engine

Trip

↓

Trip Seats

↓

Seat Allocation

↓

Seat Hold

↓

Bookings

Relationship

Trip Seat

↓

Many Holds

Trip Seat

↓

Many Segment Records

Trip Seat

↓

Many Audit Records

---

# Booking Engine

Booking

↓

Passengers

↓

Booked Seats

↓

Tickets

↓

Refunds

Relationship

Booking

↓

Many Passengers

Booking

↓

Many Seats

Booking

↓

One Payment

---

# Payment Engine

Payment

↓

Transactions

↓

Settlement

↓

Refund

Relationship

Booking

↓

One Payment

Payment

↓

Many Gateway Events

---

# Tracking Engine

Trip

↓

GPS Device

↓

Tracking History

↓

ETA

Relationship

Trip

↓

Many GPS Updates

---

# Notification Engine

Notification Template

↓

SMS

↓

Email

↓

Push

↓

WhatsApp

Relationship

Booking

↓

Many Notifications

---

# Review Engine

Customer

↓

Review

↓

Operator

↓

Trip

Relationship

Trip

↓

Many Reviews

Customer

↓

Many Reviews

---

# Settlement Engine

Operator

↓

Settlement

↓

Settlement Items

↓

Invoices

Relationship

Operator

↓

Many Settlements

Settlement

↓

Many Settlement Items

---

# Administration

Administrator

↓

Operator Approval

↓

Location Approval

↓

Audit

↓

Reports

Relationship

Administrator

↓

Many Actions

---

# Complete Business Flow

Operator

↓

Bus

↓

Layout

↓

Route

↓

Trip

↓

Trip Seats

↓

Inventory

↓

Customer Search

↓

Booking

↓

Payment

↓

Ticket

↓

Tracking

↓

Trip Completed

↓

Review

↓

Settlement