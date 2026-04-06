import streamlit as st

def pairing():
        # Constants
    p=101;
    ZERO = QuadraticFp.zero(p)
    ONE  = QuadraticFp.one(p)
    TWO = QuadraticFp(2,0,p)
    THREE = QuadraticFp(3,0,p)
    a=ONE
    b=QuadraticFp(9,0,p)
    E=[a,b]
    # Streamlit page settings
    with st.expander("Curve Definition", expanded=True): # Already True
            # 4 columns: three for inputs, one for the formula
            st.write("The prime number p and the curve are as the following in this version. We will extend them to support all possible selection in the future versions.")
            st.latex(f"p = 101")
            st.latex(f"E: y^2 \\equiv x^3 + x + 9 \\pmod{{{p}}}")
            st.markdown("</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
    points_list = [(QuadraticFp(0,0,p), QuadraticFp(3,0,p)), (QuadraticFp(0,0,p), QuadraticFp(98,0,p)), (QuadraticFp(1,0,p), QuadraticFp(27,37,p)), (QuadraticFp(1,0,p), QuadraticFp(74,64,p)), (QuadraticFp(2,0,p), QuadraticFp(25,0,p)), (QuadraticFp(2,0,p), QuadraticFp(76,0,p)), (QuadraticFp(3,0,p), QuadraticFp(49,26,p)), (QuadraticFp(3,0,p), QuadraticFp(52,75,p)), (QuadraticFp(4,0,p), QuadraticFp(28,0,p)), (QuadraticFp(4,0,p), QuadraticFp(73,0,p)), (QuadraticFp(5,0,p), QuadraticFp(51,25,p)), (QuadraticFp(5,0,p), QuadraticFp(50,76,p)), (QuadraticFp(6,0,p), QuadraticFp(19,41,p)), (QuadraticFp(6,0,p), QuadraticFp(82,60,p)), (QuadraticFp(7,0,p), QuadraticFp(37,0,p)), (QuadraticFp(7,0,p), QuadraticFp(64,0,p)) , (QuadraticFp(8,0,p), QuadraticFp(23,0,p)),(QuadraticFp(8,0,p), QuadraticFp(78,0,p)),(QuadraticFp(9,0,p), QuadraticFp(79,11,p)) , (QuadraticFp(9,0,p), QuadraticFp(22,90,p)),(QuadraticFp(10,0,p), QuadraticFp(3,0,p)) ,(QuadraticFp(10,0,p), QuadraticFp(98,0,p)),(QuadraticFp(11,0,p), QuadraticFp(51,25,p)) , (QuadraticFp(11,0,p), QuadraticFp(50,76,p)),(QuadraticFp(12,0,p), QuadraticFp(93,4,p)), (QuadraticFp(12,0,p), QuadraticFp(8,97,p)),(QuadraticFp(13,0,p), QuadraticFp(87,7,p)), (QuadraticFp(13,0,p), QuadraticFp(14,94,p)) ,(QuadraticFp(14,0,p), QuadraticFp(79,11,p)),(QuadraticFp(14,0,p), QuadraticFp(22,90,p)), (QuadraticFp(15,0,p), QuadraticFp(43,29,p)), (QuadraticFp(15,0,p), QuadraticFp(58,72,p)), (QuadraticFp(16,0,p), QuadraticFp(9,0,p)),(QuadraticFp(16,0,p), QuadraticFp(92,0,p)), (QuadraticFp(17,0,p), QuadraticFp(9,46,p)),(QuadraticFp(17,0,p), QuadraticFp(92,55,p)) ,(QuadraticFp(25,0,p),QuadraticFp(2,0,p)), (QuadraticFp(92,53,p),QuadraticFp(6,7,p))] #
    vt = (points_list[0])[1]
    st.write(vt)
    #str_points = []
    #for pt in points_list:
        #if
    str_points = [f"({pt[0]},{pt[1]})" for pt in points_list]
    all_points_str = ", ".join(str_points)
    
    # Using st.expander with expanded=True to keep it open by default
    with st.expander(f"📍 Points on curve ({len(points_list)+1} points):", expanded=True):
        # Removed the gray background div and used direct styled text
        points_html = f"""
            <div style='
                font-family: monospace; 
                font-size: 16px; 
                line-height: 1.6;
                color: #2c3e50;
                padding: 5px 0px;
                word-break: break-all;'>
                {{ {all_points_str} }}
            </div>
        """
        st.markdown(points_html, unsafe_allow_html=True)

    st.write('Enter coordinates for two points P1 and P2')
    # Get inputs
    st.write('First Point P = (xP, yP):')
    st.write('xP: a + b i')
    cols = st.columns([1, 1])
    symbol_style = "<div style='text-align: center; font-size: 24px; font-weight: bold; line-height: 45px; height: 45px;'>"
    with cols[0]: xP_real = st.number_input("xP-real", value=25, key="xP-real", label_visibility="collapsed")
    with cols[1]: xP_img = st.number_input("xP-img", value=0, key="xP-img", label_visibility="collapsed")
    st.write('yP: a + b i')
    cols = st.columns([1, 1])
    symbol_style = "<div style='text-align: center; font-size: 24px; font-weight: bold; line-height: 45px; height: 45px;'>"
    with cols[0]: yP_real = st.number_input("yP-real", value=2, key="yP-real", label_visibility="collapsed")
    with cols[1]: yP_img = st.number_input("yP-img", value=0, key="yP-img", label_visibility="collapsed")       

    #x1 = st.number_input('x1', value=0, step=1)
    #y1 = st.number_input('y1', value=0, step=1)
    P=(QuadraticFp(xP_real, xP_img, p), QuadraticFp(yP_real, yP_img, p))
    if is_on_curve(P, a, b) == False:
            st.error("The point must be on the curve.")
            #raise ValueError("The point must be on the curve. Choose another one")
    else:
        st.success(f"P = {P}")
        
    st.write('Second Point Q = (x2, y2)')
    cols = st.columns([1, 1])
    symbol_style = "<div style='text-align: center; font-size: 24px; font-weight: bold; line-height: 45px; height: 45px;'>"
    with cols[0]: xQ_real = st.number_input("xQ-real", value=92, key="xQ-real", label_visibility="collapsed")
    with cols[1]: xQ_img = st.number_input("xQ-img", value=53, key="xQ-img", label_visibility="collapsed")
    st.write('yQ: a + b i')
    cols = st.columns([1, 1])
    symbol_style = "<div style='text-align: center; font-size: 24px; font-weight: bold; line-height: 45px; height: 45px;'>"
    with cols[0]: yQ_real = st.number_input("yQ-real", value=6, key="yQ-real", label_visibility="collapsed")
    with cols[1]: yQ_img = st.number_input("yQ-img", value=7, key="yQ-img", label_visibility="collapsed")       

    Q = (QuadraticFp(xQ_real, xQ_img, p),QuadraticFp(yQ_real, yQ_img, p))
    if is_on_curve(Q, a,b) == False:
            st.error("The point must be on the curve. Choose another one")
    else:
        st.success(f"Q = {Q}")
    #st.write('The order n')
    n= st.number_input("Input n (order):", value=119)
    # Calculate
    method = st.radio("Choose Your Favorite Pairing:", ['Weil Pairing', 'Tate Pairing'], horizontal=True)
    # Apply appropriate function
    if method == 'Weil Pairing':
        f_func = weil_pairing
        description = 'weil'
        result = weil_pairing(P, Q, n, E)
        # Display result
        st.success(f'The Weil pairing W(P, Q) =  **{result}**')
        # Display more details
        st.write('### Calculation Details')
        st.latex('e_{Weil}(P, Q) = \\frac{f_P(Q)}{f_{Q}(P)},')
    else:
        f_func = tate_pairing
        description = 'tate'
        st.info(f"Tate pairing calculations is coming soon.")
        # Display more details
        st.write('### Calculation Details')
        st.latex('e_{Tate}(P, Q) = f_P(Q)^{\\frac{p^k-1}{n}}')
    


### Quadratic Fields
class QuadraticFp:
    """
    Represents elements of the form:
        a + b*i
    where i^2 = 4*i + 99
    """

    def __init__(self, a, b, p):
        self.p = p
        self.a = a %p  # real part
        self.b = b %p  # coefficient of i

    def __repr__(self):
        if self.a==0:
            if self.b==0:
                return f"0"
            else:
                return f"{self.b}i"
        elif self.b==0:
            return f"{self.a}"
        else:
            return f"{self.a} + {self.b}i"

    def __add__(self, other):
        return QuadraticFp(self.a + other.a,
                          self.b + other.b,
                          self.p)
    def __eq__(self, other):
        if isinstance(other, QuadraticFp):
            return (
                self.p == other.p and
                self.a == other.a and
                self.b == other.b
            )

        if isinstance(other, int):
            return self.a == other % self.p and self.b == 0

        return False
    def __neg__(self):
        return QuadraticFp(
            (-self.a) % self.p,
            (-self.b) % self.p,
            self.p
        )

    @classmethod
    def zero(cls, p):
        return cls(0, 0, p)

    @classmethod
    def one(cls, p):
        return cls(1,0,p)

    def __sub__(self, other):
        return QuadraticFp(self.a - other.a,
                          self.b - other.b,
                         self.p)
    def __neg__(self):
        return QuadraticFp(-self.a, -self.b, self.p)

    def __mul__(self, other):
        """
        (a + bi)(c + di)
        = ac + adi + bci + bd i^2

        Replace i^2 = 4i + 99
        """
        a, b = self.a, self.b
        c, d = other.a, other.b
        p = self.p

        real_part = a*c + b*d*99 %p
        i_part = a*d + b*c + 4*b*d %p

        return QuadraticFp(real_part, i_part, p)

    def __pow__(self, n):
        result = QuadraticFp(1, 0, self.p)
        base = self

        while n:
            if n & 1:
                result = result * base
            base = base * base
            n >>= 1

        return result
    def inverse(self):
            """
            Compute multiplicative inverse.

            If:
                x = a + b i

            We find inverse using the norm:

                N(x) = x * conjugate(x)

            For polynomial:
                i^2 - 4i - 99 = 0

            Conjugate root satisfies:
                i' = 4 - i

            So conjugate of (a + b i) is:
                a + b(4 - i)
                = (a + 4b) - b i
            """

            p = self.p
            a, b = self.a, self.b

            # conjugate
            conj = QuadraticFp(a + 4*b, -b, p)

            # norm = x * conjugate (must lie in F_p)
            norm = (self * conj).a  # imaginary part cancels

            if norm == 0:
                raise ZeroDivisionError("Element not invertible")

            norm_inv = pow(norm, p-2, p)

            return QuadraticFp(
                conj.a * norm_inv,
                conj.b * norm_inv,
                p
            )
# Constants
p=101;
ZERO = QuadraticFp.zero(p)
ONE  = QuadraticFp.one(p)
TWO = QuadraticFp(2,0,p)
THREE = QuadraticFp(3,0,p)
a=ONE
b=QuadraticFp(9,0,p)
E=[a,b]
# **Computation over EC Points**

def mod_inv(n, p):
    return pow(n, p - 2, p)


def is_on_curve(P, a, b):
    """Check whether a point lies on the curve."""
    if P is None:
        return True

    x, y = P
    return (y * y - (x * x * x + a * x + b)) == ZERO
def point_neg(P):
    """
    Compute -P on elliptic curve over F_p.
    """
    if P is None:
        return None

    x, y = P
    return (x, (-y))

def scalar_mul(k, P, a):
    """
    Compute k * P using double-and-add.
    Works for positive and negative scalars.
    """

    if k == 0 or P is None:
        return None

    # Handle negative scalar
    if k < 0:
        return scalar_mul(-k, point_neg(P), a)

    result = None  # point at infinity
    addend = P

    while k:
        if k & 1:
            result = point_add(result, addend, a)

        addend = point_double(addend, a)
        k >>= 1

    return result


def point_add(P, Q, a):
    """
    Add two points P and Q on elliptic curve over F_p.
    Curve: y^2 = x^3 + ax + b
    """
    # Handle point at infinity
    if P is None:
        return Q
    if Q is None:
        return P

    x1, y1 = P
    x2, y2 = Q

    # P + (-P) = O
    if x1 == x2 and (y1 != y2):
        return None

    # If points are equal -> doubling
    if P == Q:
        if y1==0:
            return None;
        else:
            return point_double(P, a, p)

    # Regular addition
    slope = (y2 - y1) * (x2-x1).inverse() #mod_inv(x2 - x1, p)) % p

    x3 = (slope * slope - x1 - x2)
    y3 = (slope * (x1 - x3) - y1)

    return (x3, y3)


def point_double(P, a):
    """
    Double a point P on elliptic curve over F_p.
    """
    if P is None:
        return None

    x, y = P

    # Tangent is vertical
    if y == 0:
        return None

    slope = (THREE * x * x + a) * (TWO * y).inverse()

    x3 = (slope * slope - TWO * x)
    y3 = (slope * (x - x3) - y)

    return (x3, y3)


## Miller and pairing
def line(self, R, Q , a):
    # Lets the infinity point of the elliptic curve is INF
        if Q== None:
            raise ValueError("Q must be not infinity of EC.")

        if self == None or R == None:
            if self == R:
                return ONE
            if self == None:
                return Q[0] - R[0]
            if R == None:
                return Q[0] - self[0]
        elif self != R:
            if self[0] == R[0]:
                return Q[0] - self[0]
            else:
                l = (R[1] - self[1])*(R[0] - self[0]).inverse()
                return Q[1] - self[1] - l * (Q[0] - self[0])
        else:
            numerator = (THREE*self[0]**2 + a)
            denominator = (TWO*self[1])
            if denominator == 0:
                return Q[0] - self[0]
            else:
                l = numerator*denominator.inverse()
                return Q[1] - self[1] - l * (Q[0] - self[0])
def miller(self, Q, n, a):
        if Q == None:
            raise ValueError("Q must be not infinity of EC.")
        if n == 0:
            raise ValueError("n must be nonzero.")
        n_is_negative = False
        if n < 0:
            n = -1 *n;
            n_is_negative = True

        one = 1;
        t = ONE
        V = self
        bitt_n =bin(n)[2:]
        nbin = [int(bitt_n[-i]) for i in range(1, n.bit_length()+1)];
        i = len(nbin) - 2
        while i > -1:
            S = point_double(V, a) #S = 2*V
            ell = line(V, V, Q , a) #ell = V._line_(V, Q)
            vee = line(S, point_neg(S), Q , a) #vee = S._line_(-S, Q)
            t = (t**2)*(ell*vee.inverse())
            V = S
            if nbin[i] == 1:
                S = point_add(V, self, a) # S = V+self
                ell = line(V,self, Q, a) #ell = V._line_(self, Q)
                vee = line(S, point_neg(S), Q, a) #vee = S._line_(-S, Q)
                t = t*ell*vee.inverse()
                V = S
            i = i-1
        if n_is_negative:
            vee=line(V, point_neg(V), Q)#vee = V._line_(-V, Q)
            t = (t*vee).inverse()
        return t
    
    # Weil 
def weil_pairing(P, Q, n, E):
    a,b = E[0], E[1];
    if is_on_curve(Q, a, b) == False:
        raise ValueError("points must both be on the same curve")
    # Test if P, Q are both in E[n]
    if scalar_mul(n, P, a) !=None or scalar_mul(n, Q, a)!=None:
        raise ValueError("points must both be n-torsion")

    one = 1;

    # Case where P = Q
    if P == Q:
        return one

    # Case where P = O or Q = O
    if P==None or Q == None:
        return one

    try:
        last_bit= n % 2;
        deno = miller(Q, P, n, a)
        res = QuadraticFp(-1,0,p)**last_bit*(miller(P, Q, n, a)*deno.inverse())
        return res
    except ZeroDivisionError:
        return one
    
# Tate pairing
def tate_pairing(P, Q, n, k, E):
    a,b = E[0], E[1]
    if is_on_curve(Q, a, b)== False:
        raise ValueError("Points must both be on the same curve")
    #if pow(q,k,n) != 1:
    #    raise ValueError("n does not divide (q^k - 1) for the supplied value of q")
    if scalar_mul(n, P, a)==None:
        raise ValueError("The point P must be n-torsion")
    ePQ = miller(P, Q, n, a)
    exp = int((q**k - 1)/n)
    return ePQ**exp
