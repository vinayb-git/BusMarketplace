# Bus Marketplace Master Blueprint

## 1. Product Vision

Build a bus-booking marketplace that connects passengers with verified bus operators.

The platform will allow operators to allocate selected seats to our marketplace at exclusive rates. Customers will search for buses, enter a preferred bid, compare eligible options, select seats, complete payment, and track their bus.

The platform must support:

- Indian sleeper, semi-sleeper and seater coaches
- Lower and upper berth layouts
- Intermediate boarding and dropping
- Segment-based seat availability
- Customer bidding and fare matching
- Marketplace-exclusive seat inventory
- Multi-day seat allocations
- Standardized cities, stops and boarding points
- Live bus tracking and pickup notifications
- Operator, customer and administrator portals

---

# 2. Main Users

## 2.1 Customer

The customer can:

- Register and manage a profile
- Search by origin, destination and travel date
- Enter a preferred bid amount
- View eligible buses
- Compare bus types, facilities, timings and ratings
- View scheduled and estimated arrival times
- Select boarding and dropping points
- View lower and upper berth layouts
- Select and unselect available seats
- Add passenger details
- Complete payment
- Receive booking confirmation and ticket
- Track the bus
- Receive pickup alerts
- Cancel eligible bookings
- View refunds
- View booking history
- Submit ratings and reviews

---

## 2.2 Bus Operator

The operator can:

- Register the company
- Submit business documents
- Add buses
- Add drivers and support staff
- Select the coach type
- Select or customize a seat-layout template
- Create routes
- Select standardized cities and stops
- Add boarding and dropping points
- Assign arrival and departure timings
- Create recurring trips
- Allocate seats to our marketplace
- Allocate seats for one or multiple days
- Set exclusive marketplace rates
- View bookings
- View settlements
- Update trip status
- Assign buses and drivers
- Update or share bus location
- Manage cancellations and operational changes

---

## 2.3 Platform Administrator

The administrator can:

- Approve or reject operators
- Verify operator documents
- Approve buses and drivers
- Manage location master data
- Approve new boarding-point requests
- Manage bus-layout templates
- Configure marketplace commissions
- Configure bid-matching rules
- Monitor exclusive seat allocations
- Monitor trips and live tracking
- Manage payments and settlements
- Manage refunds
- Handle complaints and disputes
- Detect duplicate inventory
- Suspend operators
- View reports and analytics
- Review audit history

---

# 3. Main Product Modules

The platform will contain the following major modules:

1. Customer application
2. Operator portal
3. Administrator portal
4. Identity and access management
5. Operator onboarding
6. Bus and coach management
7. Seat-layout engine
8. Location master
9. Route management
10. Trip scheduling
11. Inventory allocation
12. Search and bid matching
13. Segment-based seat availability
14. Booking and seat locking
15. Payment processing
16. Cancellation and refund processing
17. Settlement and commission management
18. Live tracking
19. Notification service
20. Ratings and reviews
21. Reporting and analytics
22. Audit and fraud monitoring

---

# 4. Core Customer Booking Journey

1. Customer enters origin.
2. Customer enters destination.
3. Customer selects travel date.
4. Customer enters a preferred bid.
5. System standardizes the selected locations.
6. System finds trips containing both locations.
7. System verifies that the boarding location appears before the destination.
8. System verifies boarding and dropping permissions.
9. System checks seat availability for the requested segment.
10. System calculates the segment fare.
11. System applies bid-matching rules.
12. System ranks eligible buses.
13. Customer selects a bus.
14. Customer selects pickup and drop points.
15. Customer opens the seat layout.
16. System displays lower and upper sections where applicable.
17. Customer selects one or more eligible seats.
18. System validates passenger-gender seating rules.
19. System temporarily locks selected seats.
20. Customer enters passenger details.
21. Customer completes payment.
22. System confirms the booking.
23. Customer receives a ticket and notifications.
24. Customer receives tracking and pickup alerts.
25. Trip is completed.
26. Customer can submit a rating and review.

---

# 5. Operator Onboarding

The operator must provide:

- Legal company name
- Brand or operating name
- Business registration details
- GST details where applicable
- Contact information
- Office address
- Bank account details
- Authorized representative
- Operating permits
- Insurance information
- Supporting documents

Operator statuses:

- Draft
- Submitted
- Under review
- Approved
- Rejected
- Suspended
- Inactive

An operator cannot publish trips until approval is complete.

---

# 6. Bus and Coach Configuration

## 6.1 Bus Information

Each bus should contain:

- Operator
- Registration number
- Manufacturer
- Model
- Manufacturing year
- Coach type
- Axle type
- AC or non-AC
- Total capacity
- Permit details
- Insurance details
- Amenities
- GPS capability
- Active status

---

## 6.2 Coach Types

Initial supported coach types:

- Seater
- Semi-sleeper
- Sleeper
- Seater and sleeper combination
- Multi-axle semi-sleeper
- Multi-axle sleeper

Additional attributes:

- AC
- Non-AC
- Regular axle
- Multi-axle
- Electric
- Luxury
- Volvo
- Scania
- BharatBenz or another manufacturer

AC and axle type should be stored as attributes. They should not be treated as separate seat layouts unless the physical layout differs.

---

# 7. Seat-Layout Engine

The platform must not hardcode a single seat layout.

The system will maintain reusable layout templates for:

- Seater coaches
- Semi-sleeper coaches
- Sleeper coaches
- Seater and sleeper combinations
- Lower and upper berth configurations
- Multi-axle configurations
- Custom operator layouts

When an operator selects a coach type, the system should display matching templates.

Example:

```text
Coach Type: Sleeper
Axle Type: Multi-axle
Cooling Type: AC

7.1 Layout Sections

A sleeper bus is one coach containing:

Lower berth section
Upper berth section

It is not a double-decker bus.

The booking screen may display:

Lower and upper sections side by side
Lower and upper tabs
A switch between lower and upper layouts
7.2 Seat Properties

Each seat or berth should contain:

Seat identifier
Display seat number
Seat type
Section or deck
Row
Column
X coordinate
Y coordinate
Width
Height
Orientation
Single or shared berth
Window position
Adjacent-seat identifier
Ladies-only flag if applicable
Accessible-seat flag
Active status

Seat types may include:

Standard seater
Semi-sleeper
Single sleeper
Double sleeper
Upper sleeper
Lower sleeper

Coordinates allow the interface to render different layouts without changing the application code.

7.3 Seat Display States

The customer booking screen should display:

Available seat: blank or white
Booked seat: ash or grey
Selected seat: highlighted
Temporarily held seat: unavailable
Female-booked seat: female indicator
Male-booked seat: male indicator
Blocked seat: disabled
Marketplace-unavailable seat: disabled or hidden

Customers must be able to:

Select an available seat
Tap again to unselect
Select multiple eligible seats
See the selected-seat total
See seat-level pricing
8. Passenger-Gender Seating Rules

For paired seats or berths, the system must store the exact adjacent-seat relationship.

Example:

L5 adjacent to L6
L6 adjacent to L5

A single berth has no adjacent-seat relationship.

8.1 Female Booked First

When a female passenger books one seat in a pair:

The adjacent seat can be booked only by a female passenger.
A male passenger must not be allowed to select the adjacent seat.
8.2 Male Booked First

When a male passenger books one seat in a pair:

The adjacent seat can be booked by either a male or female passenger.
8.3 Validation

The rule must be checked:

When displaying seat eligibility
When the customer selects a seat
When the seat is locked
Before payment
Before final booking confirmation

Frontend validation alone is not sufficient. The backend must validate the rule again.

9. Standardized Location Master

Operators must not freely create inconsistent city and stop names.

Examples such as:

nellore
NELLORE
Nellor
Nellore City
Nellore AP

must map to one approved location.

9.1 Location Hierarchy
Country
  State
    District
      City or Town
        Boarding and Drop Point

Example:

India
  Andhra Pradesh
    SPSR Nellore District
      Nellore
        RTC Bus Stand
        Mini Bypass
        Madras Bus Stand
9.2 Canonical Location Record

Each location should contain:

Canonical name
Display name
Location type
Country
State
District
City or town
Address
Landmark
Postal code
Latitude
Longitude
Search aliases
Active status
Approval status

Operators may search using spelling variations, but they must select an approved canonical location.

The customer should always see the approved display name.

9.3 Location Suggestions

When the operator types:

nell

The platform can suggest:

Nellore, Andhra Pradesh
Nellimarla, Andhra Pradesh
Nellikuppam, Tamil Nadu

After a city is selected, the system should suggest approved boarding and dropping points within that city.

9.4 New Location Requests

When a required boarding point does not exist, the operator can submit a request containing:

Proposed name
City
District
State
Address
Landmark
Latitude
Longitude
Map location
Supporting notes

The location remains pending until the administrator approves it.

The system should detect possible duplicates using:

Similar spelling
Existing aliases
Nearby latitude and longitude
Similar address
Same city and district
Matching landmarks
10. Route Management

A route represents an ordered path between an origin and destination.

Example:

Visakhapatnam
Vijayawada
Nellore
Tirupati
Bangalore

The operator must:

Select the origin.
Select intermediate route stops.
Select the destination.
Arrange stops in travel order.
Assign arrival and departure times.
Configure boarding permission.
Configure dropping permission.
Add pickup and drop points.
Review the complete route.
Publish the route.
10.1 Route Stop Information

Each route stop should contain:

Route
Canonical location
Stop order
Scheduled arrival
Scheduled departure
Day offset
Boarding allowed
Dropping allowed
Distance from origin
Estimated travel duration
Active status
10.2 Overnight Timing

The platform must support overnight journeys using a day offset.

Example:

Nellore
Day 0 — 9:00 PM

Ongole
Day 1 — 12:15 AM

Bangalore
Day 1 — 6:30 AM

This prevents incorrect time ordering.

10.3 Pickup and Drop Points

A city and a boarding point are different.

Example:

City: Nellore
Pickup Point: RTC Bus Stand

For every pickup or drop point, the operator should configure:

Approved location
Pickup or drop type
Scheduled time
Day offset
Contact instructions
Landmark
Boarding notes
Active status

A route stop may have multiple pickup and drop points.

11. Trip Scheduling

A route is reusable. A trip is a specific operation of that route on a date.

Each trip should contain:

Operator
Route
Bus
Driver
Service date
Scheduled start
Scheduled end
Trip status
Seat layout
Tracking status
Cancellation status
Publication status

Trip statuses may include:

Draft
Scheduled
Published
Boarding
In progress
Completed
Cancelled
Delayed
11.1 Recurring Trips

Operators should be able to create trips using:

A single date
Selected dates
A date range
Selected weekdays
A recurring schedule

Example:

August 1 to August 31
Monday through Saturday

The system creates applicable trip instances.

Special dates can be excluded or overridden.

12. Marketplace Seat Allocation

Operators can allocate selected trip seats exclusively to our marketplace.

Example:

Bus capacity: 36 berths

Allocated to our marketplace:
L1, L2, L3, L4, U1, U2, U3, U4

The remaining seats may be retained by the operator for:

Direct sales
Offline agents
Other approved channels
Internal reservations
12.1 Allocation Periods

Operators can apply an allocation to:

A single trip
Selected trip dates
A continuous date range
Selected weekdays
A recurring schedule

Example:

Seats: L1, L2, U1, U2

From: August 1
To: August 31

Days: Monday to Saturday
12.2 Allocation Rules

The system should store the operator’s selection as an allocation rule.

Allocation Rule
  Applicable dates
    Generated trips
      Trip-seat allocations

This avoids manually configuring each trip.

12.3 Allocation Ownership

Possible inventory owners:

Operator
Our marketplace
Offline agent
Other channel

Possible allocation types:

Exclusive
Shared
Operator retained
Blocked

For the first production version, marketplace allocations should be exclusive.

12.4 Seat Allocation Changes

When the operator changes a future allocation:

Already booked seats remain protected.
Temporarily held seats cannot be removed.
Future unsold seats may be updated.
The operator must see how many trips are affected.
The operator must confirm the change.
All modifications must be audited.
13. Exclusive Marketplace Pricing

For each allocated seat, the operator provides a marketplace-only rate.

The operator should confirm that:

The allocated seat is reserved for our marketplace.
The agreed rate will not be supplied to another marketplace for the same trip and seat.
Duplicate selling may result in penalties or suspension.

The exclusive rate must not be shown to the customer.

13.1 Pricing Options

The operator can configure:

One price for all selected seats
Individual price per seat
Price by seat type
Price by lower or upper section
Weekday pricing
Weekend pricing
Date-specific pricing
Festival or holiday overrides
Route-segment pricing

Example:

Monday to Thursday: ₹1,200
Friday: ₹1,400
Saturday and Sunday: ₹1,500
13.2 Commercial Visibility

The customer sees:

Final displayed fare
Bid-matching difference
Taxes
Platform fees
Final payable amount

The operator sees:

Agreed marketplace rate
Allocated inventory
Sold seats
Settlement amount

The administrator sees:

Operator rate
Customer fare
Commission
Platform margin
Taxes
Refund amount
Settlement amount
14. Bid-Matching Engine

The customer enters a preferred bid amount.

14.1 Lower Search Limit
Lower limit = Customer bid × 70%

Example:

Customer bid: ₹1,000
Lower limit: ₹700

Buses priced below the lower limit should not be shown.

14.2 Primary Acceptable Upper Limit
Upper acceptable limit = Customer bid + ₹50

All eligible buses within the lower limit and upper acceptable limit are displayed as:

+₹0
14.3 Display Difference Buckets

After the acceptable range, display differences should use standardized buckets.

Difference 0–20     → +₹0
Difference 21–70    → +₹49
Difference 71–120   → +₹99
Difference 121–170  → +₹149
Difference 171–220  → +₹199
Difference 221–270  → +₹249
Difference 271–320  → +₹299

The pattern continues in ₹50 increments.

Customers should not see arbitrary differences such as:

+₹37
+₹82
+₹116
14.4 Search Ranking

Eligible results may be ranked using:

Match to customer bid
Departure time
Arrival time
Travel duration
Operator rating
Bus rating
Seat availability
Boarding-point distance
Drop-point distance
Amenities
Cancellation policy
Reliability
Live-tracking availability
15. Intermediate Boarding and Dropping

A customer can search between any two eligible stops on a route.

The system must verify:

Both locations exist on the trip route.
Boarding stop appears before destination stop.
Boarding is allowed at the starting stop.
Dropping is allowed at the destination.
A seat is available for the entire requested segment.
The segment fare is configured or can be calculated.

Example:

Route:
Visakhapatnam
Vijayawada
Nellore
Tirupati
Bangalore

Customer search:
Nellore to Bangalore

The trip should appear when all eligibility rules pass.

16. Segment-Based Seat Availability

A seat can be sold multiple times on non-overlapping route segments.

Example:

Passenger A:
Seat L1
Visakhapatnam to Nellore

Passenger B:
Seat L1
Nellore to Bangalore

This is allowed because the segments do not overlap.

The system must prevent overlapping bookings.

Example:

Existing:
Nellore to Tirupati

New request:
Vijayawada to Bangalore

This must be rejected because the segments overlap.

17. Seat Locking

When a customer selects a seat:

The system validates availability.
The system validates the requested route segment.
The system validates passenger-gender rules.
The system places a temporary hold.
A hold-expiration time is created.
The customer proceeds to payment.

If payment is not completed:

The hold expires.
The seat becomes available again.

If payment succeeds:

The hold becomes a confirmed booking.

The booking service must prevent two customers from confirming the same seat for overlapping segments.

18. Booking Management

Each booking should contain:

Booking reference
Customer
Trip
Origin stop
Destination stop
Pickup point
Drop point
Passenger details
Seats
Fare details
Payment status
Booking status
Cancellation status
Refund status
Created time
Confirmation time

Booking statuses may include:

Pending
Seat held
Payment pending
Confirmed
Partially cancelled
Cancelled
Completed
Failed
Expired
19. Payment Processing

The payment flow should support:

UPI
Debit card
Credit card
Net banking
Wallets
Other approved payment methods

Payment statuses:

Initiated
Pending
Authorized
Successful
Failed
Cancelled
Refunded
Partially refunded

The system should use payment-provider callbacks or webhooks to confirm the final payment result.

A booking should not be confirmed based only on the customer browser response.

20. Cancellation and Refunds

Cancellation rules may depend on:

Operator
Trip
Time remaining before departure
Seat type
Fare type
Promotional conditions

The platform should show the refund amount before the customer confirms cancellation.

Refund statuses:

Not applicable
Requested
Processing
Completed
Failed
Partially refunded

Already departed segments should not be refundable unless approved by the administrator.

21. Operator Settlement

The platform should calculate:

Seats sold
Operator rate
Customer fare
Platform commission
Taxes
Payment-gateway fees
Refund deductions
Penalties
Net operator settlement

Settlement statuses:

Pending
Under review
Approved
Paid
Failed
On hold

Operators should receive a downloadable settlement statement.

22. Live Tracking

The platform should support:

GPS-device integration
Driver application location sharing
Third-party tracking providers
Manual fallback updates

The customer should see:

Scheduled pickup time
Estimated pickup time
Current bus location
Distance from pickup point
Delay
Last updated time
Trip status

Tracking access should be limited to relevant passengers and authorized users.

23. Notifications

Notifications may be sent through:

Push notification
SMS
Email
WhatsApp, where approved
In-app alerts

Notification events include:

Booking confirmation
Payment success
Payment failure
Seat-hold expiration
Trip reminder
Pickup reminder
Bus approaching
Delay
Boarding-point change
Bus change
Driver change
Trip cancellation
Refund update
Review request
24. Ratings and Reviews

Customers can rate:

Operator
Bus cleanliness
Staff behavior
Punctuality
Comfort
Boarding experience
Overall journey

Reviews should be allowed only for completed bookings.

The administrator can moderate inappropriate reviews.

25. Operator Portal Workflow

The complete operator workflow is:

Register operator
  Complete verification
    Add bus
      Select coach type
        Select layout template
          Confirm or customize seats
            Create route
              Select canonical locations
                Add pickup and drop points
                  Configure timings
                    Create trip schedule
                      Allocate seats
                        Configure exclusive rates
                          Review
                            Publish
26. Customer Search Result Information

Each search result should display:

Operator name
Bus type
AC or non-AC
Axle type
Departure time
Arrival time
Estimated timing
Duration
Boarding location
Destination
Available-seat count
Lower and upper availability
Amenities
Operator rating
Cancellation policy
Bid-match amount
Final fare
Live-tracking availability
27. Security Requirements

The platform must include:

Secure password storage
OTP verification
Role-based access
Operator-level data separation
Administrator permissions
Payment-data protection
Encryption in transit
Encryption at rest
API rate limiting
Session expiration
Device and login monitoring
Fraud detection
Audit logging
Secure document storage
Data-backup procedures

Roles may include:

Customer
Operator owner
Operator manager
Operator staff
Driver
Customer support
Finance administrator
Operations administrator
Super administrator
28. Audit Requirements

The platform should record important actions including:

Operator approval
Bus creation
Route modification
Trip publication
Seat allocation
Price changes
Inventory removal
Booking creation
Booking cancellation
Refund approval
Settlement changes
Location approval
Administrator actions

Each audit entry should contain:

User
Action
Previous value
New value
Date and time
IP address
Device information
Reason where applicable
29. Initial Technical Architecture
Customer Web and Mobile Applications
Operator Portal
Administrator Portal
              |
              v
          API Gateway
              |
    -------------------------
    |       |       |       |
 Identity Search Booking Operator
 Service  Service Service Service
    |       |       |       |
    -------------------------
              |
    -------------------------
    |       |       |       |
 Payment Inventory Route Tracking
 Service Service   Service Service
    |       |       |       |
    -------------------------
              |
    Database, Cache and Message Queue
              |
    Notifications, Analytics and Monitoring

For the first version, the services may be implemented as a modular monolith. They can later be separated into microservices as usage grows.

30. Suggested Initial Technology Stack
Frontend
React or Next.js for the customer website
React for operator and administrator portals
React Native or Flutter for mobile applications
Backend
Java with Spring Boot
REST APIs
Spring Security
JPA or Hibernate
Database
PostgreSQL
Redis for seat holds and caching
Messaging
Kafka or RabbitMQ when asynchronous processing is required
Cloud
AWS
Docker
Managed database
Object storage for documents
Central logging
Monitoring and alerting

The final stack can be adjusted before implementation.

31. Development Phases
Phase 1: Foundation
Repository structure
Master blueprint
Development environment
Database foundation
Authentication
Role management
Operator onboarding
Location master
Phase 2: Operator Configuration
Bus management
Coach types
Layout templates
Custom layout support
Route creation
Pickup and drop locations
Trip scheduling
Phase 3: Inventory and Pricing
Seat allocations
Multi-day allocations
Exclusive pricing
Trip-seat inventory
Segment availability
Operator rate management
Phase 4: Customer Booking
Search
Bid matching
Search results
Seat-layout display
Gender validation
Seat locking
Passenger information
Booking confirmation
Phase 5: Payments
Payment-gateway integration
Payment callbacks
Cancellation
Refund processing
Operator settlement
Phase 6: Journey Operations
Driver assignment
Trip status
Live tracking
Pickup alerts
Delay notifications
Phase 7: Administration
Operator approvals
Location approvals
Dispute management
Reporting
Analytics
Audit review
Phase 8: Production Readiness
Automated testing
Security testing
Performance testing
Monitoring
Backups
Disaster recovery
Deployment automation
Production launch
32. Initial MVP Scope

The first usable version should include:

Customer registration
Operator registration
Administrator approval
Location master
Bus creation
Sleeper, semi-sleeper and seater layouts
Lower and upper berth support
Route creation
Pickup and drop points
Trip scheduling
Multi-day seat allocation
Exclusive seat pricing
Customer search
Bid matching
Segment availability
Seat selection
Gender seating validation
Temporary seat locking
Payment
Booking confirmation
Basic cancellation and refund
Operator booking view
Basic administrator portal

Live tracking, advanced analytics and AI-based pricing can be added after the core booking system is stable.

33. Product Principles

The platform must follow these principles:

Operators select standardized locations instead of creating uncontrolled names.
Seat layouts must be configurable rather than hardcoded.
Lower and upper berths belong to the same sleeper coach.
Seat availability must be calculated by route segment.
Gender-based adjacent-seat restrictions must be enforced by the backend.
Allocated seats may apply to one date or multiple dates.
Exclusive operator rates must remain confidential.
Already booked seats must remain protected when allocations change.
Payment confirmation must come from the payment provider.
Every critical operator and administrator change must be audited.
The first version should be simple enough to build but structured for future growth.
Customer-facing location names must always use approved canonical names.