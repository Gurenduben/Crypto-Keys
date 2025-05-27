from ecdsa import SECP256k1, ellipticcurve
import sys

# secp256k1 parameters
n = SECP256k1.order  # curve order
curve = SECP256k1.curve
G = SECP256k1.generator  # base point

def modinv(a, modulus):
    """Modular inverse using pow."""
    try:
        return pow(a, -1, modulus)
    except ValueError:
        print(f"No modular inverse: {a} mod {modulus}")
        return None

def point_div(P, k):
    k_inv = modinv(k, n)
    if k_inv is None:
        return None
    return k_inv * P
    

def input_point():
    print("Choose a point option:")
    print("1. Use generator point G")
    print("2. Input custom point (x, y) coordinates")
    choice = input("Your choice [1/2]: ").strip()
    if choice == "1":
        return G
    elif choice == "2":
        x = int(input("Enter x coordinate: ").strip())
        y = int(input("Enter y coordinate: ").strip())
        try:
            return ellipticcurve.Point(curve, x, y)
        except Exception as e:
            print("Invalid point coordinates for secp256k1:", e)
            sys.exit(1)
    else:
        print("Invalid choice.")
        sys.exit(1)

def main():
    print("Divide an elliptic curve point by an integer (P / k):")
    P = input_point()
    k = int(input("Enter divisor (k, nonzero): ").strip())
    Q = point_div(P, k)
    if Q is not None:
        print(f"Result: P / {k} = ({Q.x()}, {Q.y()})")
        # Verify Q * k == P
        if Q * k == P:
            print("Verification: (P / k) * k == P [OK]")
        else:
            print("Verification failed: (P / k) * k != P")
    else:
        print("Could not compute P / k due to invalid input.")

if __name__ == "__main__":
    main()