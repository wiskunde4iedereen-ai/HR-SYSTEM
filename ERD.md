# Entity Relationship Diagram (ERD)

## Tables and Relationships

### 1. Users
- id (PK)
- name
- email
- hashed_password
- role
- is_active

### 2. Exporters
- id (PK)
- company_name
- owner_name
- email
- phone
- commercial_registry
- address
- is_active

### 3. Markets
- id (PK)
- country
- city
- requirements
- is_active

### 4. Products
- id (PK)
- name
- category
- hs_code
- origin
- unit
- exporter_id (FK → Exporters.id)
- is_active

### 5. Licenses
- id (PK)
- product_id (FK → Products.id)
- exporter_id (FK → Exporters.id)
- market_id (FK → Markets.id)
- status
- notes
- created_at
- approved_at

### 6. Finance
- id (PK)
- license_id (FK → Licenses.id)
- exporter_id (FK → Exporters.id)
- amount
- fee_type
- status
- created_at
- paid_at

### 7. Documents
- id (PK)
- license_id (FK → Licenses.id)
- filename
- filepath
- doc_type
- uploaded_at

## Relationships Summary

1. **Exporters 1:∞ Products** (One exporter can have many products)
2. **Exporters 1:∞ Licenses** (One exporter can have many licenses)
3. **Markets 1:∞ Licenses** (One market can have many licenses)
4. **Products 1:∞ Licenses** (One product can have many licenses)
5. **Licenses 1:∞ Finance** (One license can have many financial records)
6. **Licenses 1:∞ Documents** (One license can have many documents)

## Key Notes
- PK = Primary Key
- FK = Foreign Key
- The `users` table appears to be for authentication/authorization and is not directly related to the business entities in this schema
- Core business flow: Exporter creates Product → Applies for License (to specific Market) → Finance tracks payments → Documents are attached to licenses