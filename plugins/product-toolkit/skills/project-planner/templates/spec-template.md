# Checkout Redesign — PRD

## Overview
Reduce checkout drop-off on mobile by 20% by streamlining the form, adding wallet payments, and improving error handling.

## Requirements
- Users must be able to check out as a guest (no account required).
- The system should support Apple Pay and Google Pay on supported devices.
- Show a sticky order summary on screens under 768px.
- Validate addresses against the USPS API before allowing payment.
- Persist in-progress checkouts to sessionStorage so a refresh doesn't lose state.
- All form errors must be announced to screen readers via aria-live regions.
- The application should show a clear loading state during payment authorization.
- Implement a webhook endpoint to receive payment confirmations from Stripe.
- Add a database migration to store a checkout_session_id on the orders table.
- Display an order confirmation screen with the estimated delivery date.

## Non-goals
- Subscription billing (deferred to v2).
- Multi-currency support is out of scope for this release.
