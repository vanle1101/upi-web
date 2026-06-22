"""Smoke: verify AccountAlreadyExistsError + ACCOUNT_EXISTS_MSG wiring."""
import sys
import browser_phase as bp
import signup

assert issubclass(bp.AccountAlreadyExistsError, bp.BrowserPhaseError), "phai la subclass"
assert hasattr(bp, "ACCOUNT_EXISTS_MSG"), "thieu ACCOUNT_EXISTS_MSG"
assert "Khong tao tai khoan moi" in bp.ACCOUNT_EXISTS_MSG
# signup.py phai import duoc class
assert signup.AccountAlreadyExistsError is bp.AccountAlreadyExistsError

# message khi raise se la tieng Viet thuan, str(exc) khong co ten class
e = bp.AccountAlreadyExistsError(f"{bp.ACCOUNT_EXISTS_MSG} (da bat 2FA).")
assert str(e).startswith("Khong tao tai khoan moi")
print("OK ACCOUNT_EXISTS_MSG:", bp.ACCOUNT_EXISTS_MSG)
print("ALL PASS")
