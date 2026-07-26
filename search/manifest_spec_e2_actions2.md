# 掃引 ① r2 の spec 追補 2(A 上の作用と構造定数 — 定義のみ)

## 1. Hall 基底と Hall 基底の順序

**`docs/命題_E22三段判定_v1.md` 命題 E22.5(p195–205)**

$P^{(5)}:=F_2/\gamma_6$, $A:=\gamma_2/\gamma_6$ の Hall 基底(順序を正本として固定):
$$w;\quad p,q;\quad r_1,r_2,r_3;\quad t_1=[r_1,x],t_2=[r_1,y],t_3=[r_2,y],t_4=[r_3,y];\quad t_5:=[w,p],\ t_6:=[w,q].$$

重み $2;3;4;5;5$、$\mathbb Z$-階数 $1+2+3+6=12$。

---

## 2. 交換子対 $\beta$ の定義と明示形

**`docs/命題_E22三段判定_v1.md` 節 1(p39–45) / 節 5.4(p238–243)**

**交換子対の定義**:
$$\beta:\bar A\times\bar A\to C,\quad \beta(\bar u,\bar v):=[u,v]=u^{-1}v^{-1}uv.$$
$\text{class}\ 2$ より $[uz,vz']=[u,v]$ ($z,z'\in C$)なので well-defined、双加法的、交代的($\beta(\bar u,\bar u)=0$、$\beta(\bar v,\bar u)=-\beta(\bar u,\bar v)$)。

**対称性の破れ**:
$$c_s(\bar u,\bar v)=c_s(\bar v,\bar u)\cdot\beta(\bar u,\bar v).$$

**明示形(Hall 座標)** ($\bar u=u_w w+u_p p+u_q q+\cdots$ と書く):
$$\boxed{\ \beta(\bar u,\bar v)=(u_wv_p-u_pv_w)\,t_5+(u_wv_q-u_qv_w)\,t_6\ }.$$

---

## 3. σ と θ の $C$ 上の作用

**`docs/命題_E22三段判定_v1.md` 節 5.2(p207–220) / `docs/week4-E2作戦_v3.md` 節 2.2(p87–90)**

$C:=\langle t_5,t_6\rangle\cong\mathbb Z^2$ は中心なので $\mathrm{Ad}(\bar Y^m)$ と $\iota_{X^u}$ は $C$ 上恒等、したがって $\sigma\vert_C=\tau\vert_C$ で $\langle\sigma,\theta\rangle$ は $C$ 上真に $S_3$ を通す。基底 $(t_5,t_6)$ に対し:
$$\sigma\vert_C=\begin{pmatrix}0&-1\\1&-1\end{pmatrix},\qquad \theta\vert_C=\begin{pmatrix}0&1\\1&0\end{pmatrix}.$$

**明示的な基底元の像**:
- $\sigma(t_5)=[\sigma w,\sigma p]=[w,q]=t_6$ (重み 6 以上を落とすと)
- $\sigma(t_6)=[\sigma w,\sigma q]=[w,p^{-1}q^{-1}]=t_5^{-1}t_6^{-1}$
- $\theta(t_5)=[w^{-1},q^{-1}]=[w,q]=t_6$
- $\theta(t_6)=[w^{-1},p^{-1}]=[w,p]=t_5$

---

## 4. Section の定義と Section cocycle

**`docs/命題_E22三段判定_v1.md` 節 1(p41–45) / `docs/week4-掃引宇宙_v3.md` 節 1.3(p60–68)**

**Section**:
写像 $s:\bar A\to A$ で $\pi_C\circ s=\mathrm{id}$, $s(0)=1$。各 $f\in A$ は $f=s(\bar f)z$ ($z\in C$)と一意に書ける。

**Canonical section (Hall 正規形 — 順序と代表元区間を正本とする)**:
$$s(\bar a)=w^{a_1}p^{a_2}q^{a_3}r_1^{a_4}r_2^{a_5}r_3^{a_6}t_1^{a_7}t_2^{a_8}t_3^{a_9}t_4^{a_{10}},\qquad 0\le a_i<2^j.$$

**Section cocycle**:
$$c_s(\bar u,\bar v):=s(\bar u)\,s(\bar v)\,s(\bar u+\bar v)^{-1}\in C.$$

---

## 5. 二欠損 $q_\theta, q_N$ の定義

**`docs/命題_E22三段判定_v1.md` 節 3.2(p88–97) / `docs/week4-掃引宇宙_v3.md` 節 1.4(p70–74)**

$\bar f\in\mathcal L$ に対し、**欠損対**を
$$\Xi(\bar f):=\Bigl(\ \underbrace{\theta(s\bar f)\,s\bar f}_{=:q_\theta(\bar f)}\ ,\ \underbrace{E_m\,\sigma^2(s\bar f)\sigma(s\bar f)\,s\bar f}_{=:q_N(\bar f)}\ \Bigr)\in C\times C.$$

**中心元の分離** (`docs/命題_E22三段判定_v1.md` 補題 E22.2, p72–76):
$$D_\theta(uz)=D_\theta(u)\cdot(1+\theta)z,\quad \text{ここで } (1+\theta)z:=\theta(z)z.$$
$$\mathcal N(uz)=\mathcal N(u)\cdot\mathcal N_C(z),\quad \text{ここで } \mathcal N_C(z):=\sigma^2(z)\sigma(z)z.$$

$C$ は可換で $\sigma,\theta$-安定なので、両者は $C$ 上の群準同型である。

---

## 原本に明示的な定義式がない項目

- $E_m$ の**明示式**(提言箇所 `命題_E22三段判定_v1.md` では「$E_m\in A^σ$」の存在主張のみ、class-4 の閉形式 `week4-E2作戦_v3.md p221` は metabelian 限定版で class-5 非可換版はなし)
- $A$ の全体(重み 4 以上を含む)における $σ,θ$ の**明示的な基底元別像**(記載は $C$ 上のみ + $w,p,q$ の定性記述)
- Hall 基底の**乗法規則と交換子 commutator table の閉形**(Magnus formula または Hall collection の「規則」として参照されるが、本文で明示式を見つけない)

---

**抽出完了**: 定義 5 件 + 見つからない 3 件。§1–§5 の 5 セクション、計 13 行の逐語複製。
