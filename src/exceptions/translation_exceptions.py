from fastapi import HTTPException, status


def raise_translation_not_found_exception():
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Translation not found.")


def raise_forbidden_exception():
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access to this resource is not allowed.")
