# Source Reputation Ledger

This ledger is automatically maintained by `curator-feedback-loop`. When a website/author/account accumulates 3 D or E grade ratings during `curator-filter` blind review, its identifier (domain/author) is added to the Blacklist.
Blacklisted entities are immediately intercepted and routed to `03_NOISE` in future filter runs, saving token consumption.

## Strikes (Under Observation)
| Domain/Author | Strikes | Last Flagged Reason | Related Article |
|---|---|---|---|
| e.g.: x.com/bot_account | 1 | Pure hype, no facts | 20260331_BTC_100k.md |

## Blacklist (Permanently Blocked)
| Domain/Author | Blocked Date | Reason |
|---|---|---|
| (no entries yet) | | |

*If the user rehabilitates a source via `SUPERVISOR_FEEDBACK`, its strike count will be reset to zero.*
