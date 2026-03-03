from sqlalchemy.orm import Session
from sqlalchemy import func
from models import Item, Claim
from schemas import ItemIn, ClaimIn, ItemStats

# ✅ PROVIDED
def get_all_items(db: Session, skip: int = 0, limit: int = 10) -> list[Item]:
    return db.query(Item).offset(skip).limit(limit).all()

# ✅ PROVIDED
def get_one_item(db: Session, item_id: int) -> Item | None:
    return db.query(Item).filter(Item.id == item_id).first()

# ✅ PROVIDED
def get_claims_for_item(db: Session, item_id: int) -> list[Claim]:
    return db.query(Claim).filter(Claim.item_id == item_id).all()

# TODO #1 — Implement create_item()
# Hints:
#   - Build an Item ORM object from item_in.model_dump()
#   - Use db.add(), db.commit(), db.refresh(), return the new item

# DONE
def create_item(db: Session, item_in: ItemIn) -> Item:
    db_item = Item(name=item_in.name, description=item_in.description, category=item_in.category,
                   location=item_in.location, status=item_in.status, resolved=item_in.resolved,
                   date_lost=item_in.date_lost)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


# TODO #2 — Implement update_item()
# Hints:
#   - Use get_one_item() to fetch; return None if not found
#   - Loop over item_in.model_dump().items() and use setattr()
#   - Commit, refresh, and return the updated item

# DONE
def update_item(db: Session, item_id: int, item_in: ItemIn) -> Item | None:
    db_item = get_one_item(db, item_id)
    if db_item is None:
        return None
    
    for field, value in item_in.model_dump().items():
        setattr(db_item, field, value)
    
    db.commit()
    db.refresh(db_item)
    return db_item
    
# TODO #3 — Implement delete_item()
# Hints:
#   - Fetch with get_one_item(); return False if not found
#   - db.delete() + db.commit(), return True
#   - Cascade in models.py will auto-delete all related claims

# DONE
def delete_item(db: Session, item_id: int) -> bool:
    db_item = get_one_item(db, item_id)
    if db_item is None:
            return False
    db.delete(db_item)
    db.commit()
    return True

# TODO #4 — Implement create_claim()
# Hints:
#   - Build a Claim ORM object using claim_in.model_dump(), set item_id
#   - db.add(), db.commit(), db.refresh(), return the new claim

# DONE
def create_claim(db: Session, item_id: int, claim_in: ClaimIn) -> Claim:
    claim = claim_in.model_dump()
    claim["item_id"] = item_id
    db_claim = Claim(**claim)

    db.add(db_claim)
    db.commit()
    db.refresh(db_claim)
    return db_claim

# TODO #5 — Implement get_unresolved_items()
# Hints:
#   - Query Item where Item.resolved == False
#   - Apply skip and limit, return the list

# DONE
def get_unresolved_items(db: Session, skip: int = 0, limit: int = 10) -> list[Item]:
    return (
        db.query(Item).filter(Item.resolved == False).offset(skip).limit(limit).all()
    )

# TODO #6 — Implement get_item_stats()
# Hints:
#   - Fetch the item using get_one_item(); return None if not found
#   - Use db.query(func.count(Claim.id)).filter(Claim.item_id == item_id)
#     for total_claims
#   - Add a second filter for Claim.approved == True to count approved claims
#   - Return an ItemStats object built manually (not an ORM object)

# DONE
def get_item_stats(db: Session, item_id: int):
    db_item = get_one_item(db, item_id)
    if db_item is None:
        return None
    # Use db.query(func.count(Claim.id)).filter(Claim.item_id == item_id)
    # for total_claims
    total_claims = (
        db.query(func.count(Claim.id)).filter(Claim.item_id == item_id).scalar()
    )

    approved_count = (
        db.query(func.count(Claim.id)).filter(Claim.item_id == item_id, Claim.approved.is_(True)).scalar()
    )
    return ItemStats(
        item_id=item_id,
        name=db_item.name,
        total_claims=total_claims,
        approved=approved_count,
        resolved=db_item.resolved,
    )

# Delete claim was missing
def delete_claim(db: Session, item_id: int, claim_id: int) -> bool:
    claim = (
        db.query(Claim)
        .filter(Claim.id == claim_id, Claim.item_id == item_id)
        .first()
    )
    if claim is None:
        return False

    db.delete(claim)
    db.commit()
    return True
