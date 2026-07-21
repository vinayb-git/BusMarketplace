# Bus Marketplace Business Rules

## 1. Document Purpose

This document defines the detailed business rules for the Bus Marketplace platform.

These rules will be used by:

- Product owners
- Developers
- Testers
- Operators
- Administrators
- Support teams

Each rule must be clear, testable, and traceable.

---

## 2. Rule Format

Each business rule should follow this format:

```text
Rule ID:
Rule Name:
Description:
Actors:
Trigger:
Conditions:
Expected Result:
Exceptions:
Validation Point:
Priority:
Status:

3. Business Rule Categories

The rules will be organized under the following categories:

User Registration and Authentication
Operator Onboarding
Bus Management
Coach Type and Layout
Location Master
Route Management
Pickup and Drop Points
Trip Scheduling
Seat Allocation
Exclusive Inventory
Pricing
Bid Matching
Search Eligibility
Segment Availability
Gender-Based Seating
Seat Locking
Booking
Payment
Cancellation
Refund
Settlement
Notifications
Tracking
Reviews
Administration
Audit
Security
Reporting
Fraud Prevention
Future Enhancements
4. Initial Business Rules
BR-LOC-001 — Canonical Location Selection

Description:
Operators must select cities, towns, route stops, pickup points, and drop points from the approved location master.

Actors:
Operator, Administrator

Trigger:
An operator creates or updates a route.

Conditions:
The required location exists in the approved location master.

Expected Result:
The operator selects the approved canonical location instead of entering unrestricted text.

Exceptions:
If the location does not exist, the operator may submit a new-location request.

Validation Point:
Frontend and backend

Priority:
Critical

Status:
Approved

BR-LOC-002 — Standardized Location Display

Description:
The platform must display the approved canonical location name to customers.

Actors:
Customer, Operator, Administrator

Trigger:
A location is displayed in search, booking, ticketing, tracking, or reporting.

Expected Result:
Incorrect capitalization, spelling variations, and operator-entered aliases must not appear as customer-facing location names.

Validation Point:
Backend response and frontend display

Priority:
Critical

Status:
Approved

BR-ROUTE-001 — Ordered Route Stops

Description:
Every route must contain an ordered list of stops from origin to destination.

Actors:
Operator

Trigger:
The operator creates or updates a route.

Expected Result:
Each stop receives a unique stop order.

Validation Point:
Backend

Priority:
Critical

Status:
Approved

BR-ROUTE-002 — Intermediate Search Eligibility

Description:
A trip may appear for an intermediate search only when the boarding stop appears before the destination stop.

Actors:
Customer

Trigger:
A customer searches for a trip.

Expected Result:
The trip is excluded when the selected destination appears before the boarding stop.

Validation Point:
Search service

Priority:
Critical

Status:
Approved

BR-TIME-001 — Arrival and Departure Timing

Description:
Every route stop must contain scheduled arrival and departure timing where applicable.

Actors:
Operator

Trigger:
A route schedule is created.

Expected Result:
The system validates chronological order across all route stops.

Validation Point:
Frontend and backend

Priority:
Critical

Status:
Approved

BR-TIME-002 — Overnight Day Offset

Description:
Trips crossing midnight must use a day offset.

Actors:
Operator

Trigger:
A stop time is earlier than the previous stop’s clock time.

Expected Result:
The operator must assign the correct next-day offset.

Validation Point:
Backend

Priority:
Critical

Status:
Approved

BR-LAYOUT-001 — Template-Based Layout

Description:
Operators must select an approved seat-layout template matching the coach type.

Actors:
Operator, Administrator

Trigger:
A bus is configured.

Expected Result:
The applicable seater, semi-sleeper, sleeper, or combination layout is displayed.

Validation Point:
Operator portal and backend

Priority:
Critical

Status:
Approved

BR-LAYOUT-002 — Lower and Upper Sleeper Sections

Description:
A sleeper coach may contain lower and upper berth sections within the same bus.

Expected Result:
The booking interface must represent both sections clearly.

Priority:
Critical

Status:
Approved

BR-SEAT-001 — Seat Display State

Description:
Available seats must appear blank, booked seats must appear ash or grey, and selected seats must appear highlighted.

Actors:
Customer

Trigger:
The customer opens the seat layout.

Expected Result:
The current seat state is displayed accurately.

Validation Point:
Frontend and booking service

Priority:
Critical

Status:
Approved

BR-SEAT-002 — Seat Select and Unselect

Description:
A customer may select an available seat and unselect it before proceeding to payment.

Expected Result:
The selected-seat summary and total fare are updated immediately.

Priority:
High

Status:
Approved

BR-GENDER-001 — Female Passenger Booked First

Description:
When a female passenger books one seat in a paired-seat arrangement, the adjacent seat may be booked only by a female passenger.

Actors:
Customer

Trigger:
A customer attempts to select the adjacent seat.

Expected Result:
Male selection is blocked.

Validation Point:
Seat display, seat hold, payment validation, and booking confirmation

Priority:
Critical

Status:
Approved

BR-GENDER-002 — Male Passenger Booked First

Description:
When a male passenger books one seat in a paired-seat arrangement, the adjacent seat may be booked by either a male or female passenger.

Expected Result:
No gender restriction is applied to the adjacent available seat.

Validation Point:
Backend

Priority:
Critical

Status:
Approved

BR-ALLOC-001 — Marketplace Seat Allocation

Description:
Operators may allocate selected seats exclusively to the marketplace.

Actors:
Operator

Trigger:
The operator configures trip inventory.

Expected Result:
The selected seats are marked as marketplace-owned inventory.

Validation Point:
Inventory service

Priority:
Critical

Status:
Approved

BR-ALLOC-002 — Multi-Day Allocation

Description:
Operators may allocate seats for a single date, selected dates, a date range, or a recurring weekday schedule.

Expected Result:
The system applies the allocation rule to all matching future trips.

Priority:
Critical

Status:
Approved

BR-ALLOC-003 — Protect Existing Bookings

Description:
Allocation changes must not remove or modify seats that are already booked or temporarily held.

Validation Point:
Inventory service

Priority:
Critical

Status:
Approved

BR-PRICE-001 — Exclusive Operator Rate

Description:
Operators must provide an exclusive marketplace rate for every allocated seat or seat group.

Expected Result:
The rate is stored confidentially and is not shown directly to the customer.

Priority:
Critical

Status:
Approved

BR-BID-001 — Bid Lower Limit

Description:
The lower search limit is seventy percent of the customer’s bid.

Formula:

Lower Limit = Bid Amount × 70%

Priority:
Critical

Status:
Approved

BR-BID-002 — Primary Acceptable Range

Description:
Eligible fares between the lower limit and the customer bid plus ₹50 are displayed with a +₹0 indicator.

Formula:

Upper Acceptable Limit = Bid Amount + ₹50

Priority:
Critical

Status:
Approved

BR-SEGMENT-001 — Segment Seat Reuse

Description:
A seat may be sold again for a non-overlapping route segment.

Expected Result:
The same seat can be assigned to multiple passengers when their travel segments do not overlap.

Priority:
Critical

Status:
Approved

BR-SEGMENT-002 — Overlap Prevention

Description:
The platform must reject a booking when the requested seat segment overlaps an existing booking or hold.

Validation Point:
Inventory and booking services

Priority:
Critical

Status:
Approved

BR-HOLD-001 — Temporary Seat Hold

Description:
Selected seats must be temporarily held during checkout.

Expected Result:
Other customers cannot reserve the same seat for an overlapping segment during the hold period.

Priority:
Critical

Status:
Approved

BR-HOLD-002 — Hold Expiration

Description:
A seat hold must expire automatically when payment is not completed within the allowed period.

Expected Result:
The seat becomes available again.

Priority:
Critical

Status:
Approved

BR-PAY-001 — Payment Confirmation Source

Description:
A booking may be confirmed only after receiving successful confirmation from the payment provider.

Expected Result:
The browser response alone must not confirm a booking.

Priority:
Critical

Status:
Approved

BR-AUDIT-001 — Critical Change Logging

Description:
Critical operator and administrator actions must be recorded in the audit log.

Expected Result:
The audit record contains the user, action, previous value, new value, date, time, and source information.

Priority:
Critical

Status:
Approved