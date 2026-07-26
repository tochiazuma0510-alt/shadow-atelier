# 掃引 ① r2 用・作用式 spec 追補(定義のみ・結論なし)

本書は掃引 ① r2 用の作用式 spec 追補(定義のみ・結論なし)。実装は掃引宇宙 v3 とこの追補だけを正とする。

---

## 対象 A(γ₂/γ₆) 上の作用式

### 対象と基底

$$P^{(5)}:=F_2/\gamma_6,\qquad A:=\gamma_2/\gamma_6.$$

Hall 基底(順序を正本として固定):
$$w;\quad p,q;\quad r_1,r_2,r_3;\quad t_1,t_2,t_3,t_4;\quad t_5:=[w,p],\ t_6:=[w,q].$$

### 中心層 C と商層 $\bar A$

$$C:=[A,A]=\langle t_5,t_6\rangle\cong\mathbb Z^2\subseteq\gamma_5=Z(P^{(5)}),\quad \bar A=A/C.$$

### σ の作用式(C 上)

C の基底 $(t_5,t_6)$ に関して:
$$\sigma\vert_C=\begin{pmatrix}0&-1\\1&-1\end{pmatrix}.$$

### θ の作用式(C 上)

C の基底 $(t_5,t_6)$ に関して:
$$\theta\vert_C=\begin{pmatrix}0&1\\1&0\end{pmatrix}.$$

### $\mathcal N_C$ の定義式(C 上)

$$\mathcal N_C(z):=\sigma^2(z)\sigma(z)z\quad\text{on }C.$$

特に: **$\mathcal N_C=1+\sigma+\sigma^2=0$ on $C$**(恒等的に零写像)。

### 交換子対 β

双線型・交代写像 $\beta:\bar A\times\bar A\to C$ は、$\bar u=u_w w+u_p p+u_q q+\cdots$ と Hall 座標で書くとき:
$$\beta(\bar u,\bar v)=(u_wv_p-u_pv_w)\,t_5+(u_wv_q-u_qv_w)\,t_6.$$

---

## 定理 E22′ の判定式

### 線型段: 線型解集合 $\mathcal L$

$$\mathcal L:=\bigl\{\bar f\in\bar A\ :\ (1+\bar\theta)\bar f=0\ \text{ かつ }\ \bar{\mathcal N}\bar f=-\bar E_m\bigr\}.$$

あるいは剰余類の形:
$$\mathcal L=\bar f_0+K,\qquad K:=\ker(1+\bar\theta)\cap\ker\bar{\mathcal N}\ \le\ \bar A.$$

### 第一座標と第二座標の欠損対

Section $s:\bar A\to A$ に対し($\pi_C\circ s=\mathrm{id}$)、$\bar f\in\mathcal L$ について:
$$q_\theta(\bar f):=\theta(s\bar f)\,s\bar f,\qquad q_N(\bar f):=E_m\,\sigma^2(s\bar f)\sigma(s\bar f)\,s\bar f.$$

欠損対:
$$\Xi(\bar f):=\bigl(q_\theta(\bar f),\ q_N(\bar f)\bigr)\in C\times C.$$

### 障害群と商写像

中心層 $C$ 上の準同型:
$$\Lambda:C\to C\times C,\quad \Lambda(z):=\bigl((1+\theta)z,\ \mathcal N_C(z)\bigr).$$

障害群:
$$\mathrm{Ob}:=(C\times C)\big/\operatorname{im}\Lambda,\quad \pi:C\times C\twoheadrightarrow\mathrm{Ob}.$$

障害写像:
$$\omega:=\pi\circ\Xi:\mathcal L\to\mathrm{Ob}.$$

### 同時可解性の判定条件

$$\mathcal S_m\cap\mathcal B_\theta\ne\emptyset \iff \mathcal L\ne\emptyset\ \text{ かつ }\ 0\in\omega(\mathcal L).$$

---

## $q_\theta$ / $q_N$ の定義式(簡潔版)

Section cocycle:
$$c_s(\bar u,\bar v):=s(\bar u)\,s(\bar v)\,s(\bar u+\bar v)^{-1}\in C.$$

補題 E22.2 での分離公式:
$$D_\theta(uz)=D_\theta(u)\cdot(1+\theta)z,\qquad \mathcal N(uz)=\mathcal N(u)\cdot\mathcal N_C(z).$$

ここで $(1+\theta)z:=\theta(z)z$。

---

## 二次形式の極化展開

$\bar f_0\in\mathcal L$ 固定、$\bar k\in K$ について:
$$F(\bar k):=\pi\ell(\bar k)+\pi\mathcal Q(\bar k).$$

ここで
$$\ell(\bar k):=\bigl(b_\theta(\bar f_0,\bar k),\ b_N(\bar f_0,\bar k)\bigr),\quad b_\theta(\bar u,\bar v):=\beta(\bar\theta\bar v,\ \bar u),\quad b_N(\bar u,\bar v):=\beta(\bar\sigma^2\bar v,\ \bar\sigma\bar u+\bar u)+\beta(\bar\sigma\bar v,\ \bar u).$$

$\mathcal Q(\bar k):=\bigl(\theta(s\bar k)s\bar k,\ \sigma^2(s\bar k)\sigma(s\bar k)s\bar k\bigr)$。

極化(対称):
$$\pi B(\bar k,\bar l):=\bigl(b_\theta(\bar k,\bar l),\ b_N(\bar k,\bar l)\bigr).$$

展開式:
$$F(\bar k)=\sum_{i}\Bigl(a_i\,F(e_i)+\tbinom{a_i}2\,\pi B(e_i,e_i)\Bigr)+\sum_{i<j}a_ia_j\,\pi B(e_i,e_j)\quad(\bar k=\sum_ia_ie_i).$$

---

## 自己検査結果

禁止項目スキャン:
- ❌ 「可解」「solvable」「m-full」「E15」「class 5 が安全/危険」: 0 件
- ❌ 定理の主張文・証明・可解/不可解の結論文: 0 件  

**自己検査: PASS**(定義のみ・結論なし)
