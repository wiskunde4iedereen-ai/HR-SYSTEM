# PROJECT_MAP - نظام قاعدة البيانات الذكية للهيئة

## [TECH_STACK]
| الطبقة | التقنية | الإصدار |
|--------|---------|---------|
| Backend | FastAPI | 0.136.3 |
| ORM | SQLAlchemy (sync) | 2.0.50 |
| Database (dev) | SQLite | - |
| Database (prod) | MySQL | 8+ |
| Auth | JWT + bcrypt | - |
| Validation | Pydantic v2 | built-in |
| Frontend | Jinja2 + Bootstrap 5 (RTL) | - |
| Color Theme | Syrian flag: dark green (#1a5632), black (#1a1a1a), gold (#c8962e) | - |
| Logging | structlog | latest |
| Server | Uvicorn | 0.48.0 |
| Language | Python | 3.12.10 |
| Encoding | UTF-8 (Arabic support) | - |

## [SYSTEM_FLOW]
```
Client → FastAPI → SQLAlchemy (sync) → SQLite/MySQL
                ↕
          Jinja2 Templates (RTL Arabic, Bootstrap 5, Syrian flag theme)
                ↕
          JWT Auth Middleware (Cookie + Header)
                ↕
          structlog Logger
```

## [UI THEME]
- Primary color: Dark green (`#1a5632`, `#267a48`) — navbar, card headers, primary cards
- Secondary color: Black (`#1a1a1a`) — stat cards, text
- Accent color: Gold (`#c8962e`, `#daa940`) — buttons, badges, highlight cards
- Background: Off-white (`#f5f5f0`)
- CSS classes: `bg-syria-green`, `bg-syria-gold`, `bg-syria-black`, `btn-gold`, `text-syria-gold`

## [ARCHITECTURE]
### Domain Modules — ALL DONE
1. **auth** ✅ - تسجيل دخول، خروج، JWT، RBAC (admin/employee/exporter/importer)، مع إضافة حقل الراتب للموظف
2. **exporters** ✅ - إدارة المصدرين (إضافة/تعديل/حذف/بحث)
3. **products** ✅ - إدارة المنتجات (إضافة/تعديل/حذف/بحث)
4. **markets** ✅ - إدارة الأسواق الخارجية (إضافة/تعديل/حذف)
5. **licenses** ✅ - إدارة التراخيص (تقديم طلب، اعتماد، رفض)
6. **finance** ✅ - إدارة السجلات المالية (رسوم، تسديد)
7. **documents** ✅ - رفع وتحميل المستندات
8. **reports** ✅ - لوحة إحصائيات + تصدير CSV
9. **integrations** — خارج النطاق الحالي

### Role-Based Dashboards
| Role | Dashboard Template | Nav Bar |
|------|-------------------|---------|
| admin / developer | `dashboard/index.html` (full stats, 6 cards with links) | Full nav (8 items) |
| employee | `dashboard/employee.html` (simplified, 4 cards) | Full nav (all items) |
| exporter / importer | `dashboard/index.html` (stats only, no nav access to CRUD) | Full nav (routes protected by `require_role`) |

## [ORPHANS & PENDING]
- AI Forecasting للتصدير
- Mobile Application
- تكامل دولي مباشر
- تكامل OCR للمستندات
- تكامل مع جهات حكومية (API خارجية)
