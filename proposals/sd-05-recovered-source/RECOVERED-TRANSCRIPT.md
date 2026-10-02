<!--
RECOVERED DESIGN INTENT — SD-05
SOURCE: conversation transcription supplied by the author during the 2026-10-02
        audit session. NOT a contemporaneous artifact.
STATUS: recovered / non-primary
This file is preserved as recovered. It has not been cleaned, normalised,
corrected, or reordered. Any later reading must not treat it as a
specification that existed alongside the implementation.
-->

## 2. Metodología: Engine de Riesgo Adaptativo

Para evitar el cuello de botella de latencia y gas de registrar *todas* las
ejecuciones *on-chain*, definimos la función de escalado de riesgo no lineal
$r_i \in [0, 1]$:

$$r_i = \sigma \left( w_1 U_i + w_2 V_i + w_3 I_i + w_4 N_i + w_5 P_i + \gamma (U_i \cdot V_i) \right)$$

#### Vector de Variables

* $U_i \in [0, 1]$ (Uncertainty): Entropía de log-probs del modelo o varianza de respuestas.
* $V_i \in [0, 1]$ (Value): Escalar normalizado del valor monetario/recursos comprometidos en la acción.
* $I_i \in [0, 1]$ (Impact): Severidad del impacto (0 = Consulta *read-only*; 1 = Mutación de base de datos / transferencia de activos).
* $N_i \in [0, 1]$ (Novelty): Distancia del vector de entrada respecto a la memoria semántica histórica (*Out-of-Distribution score*).
* $P_i \in [0, 1]$ (Policy Sensitivity): Proximidad del input/output a los límites de restricciones de seguridad (*Guardrail Margin*).

#### Políticas de Activación por Umbral ($\theta$)

| Nivel de Riesgo | Condición | Mecanismo de Atestación | Overhead Estimado | Costo On-Chain |
| --- | --- | --- | --- | --- |
| **$L_0$: Low Risk** | $r_i < 0.30$ | **Local Receipt:** Log local con hash en cadena local. | $< 1\text{ ms}$ | $\$0.00$ |
| **$L_1$: Medium Risk** | $0.30 \le r_i < 0.65$ | **Signed Receipt:** Recibo con firma Ed25519 del agente distribuido off-chain. | $2-5\text{ ms}$ | $\$0.00$ |
| **$L_2$: High Risk** | $0.65 \le r_i < 0.85$ | **On-Chain Anchoring:** Asignación del $TraceRoot$ en Smart Contract en L2/Stellar. | $200-800\text{ ms}$ | Gas estándar ($\sim 10^{-5}\ \text{USD}$) |
| **$L_3$: Critical** | $r_i \ge 0.85$ | **Multi-Party Attestation:** Requiere $k$-de-$n$ firmas de agentes auditores antes de ejecutar la acción *on-chain*. | $1000-2500\text{ ms}$ | Multi-sig gas |

#### B. Script de Ingesta, Merkle Tree y Verificador (Python)

```python
class AdaptiveRiskEngine:
    def __init__(self, weights: list = [0.2, 0.3, 0.3, 0.1, 0.1]):
        self.w = weights

    def compute_risk(self, u: float, v: float, i: float, n: float, p: float) -> float:
        raw_score = (self.w[0]*u + self.w[1]*v + self.w[2]*i + self.w[3]*n + self.w[4]*p) + (0.15 * u * v)
        return min(max(raw_score, 0.0), 1.0)
```

## 4. Matriz de Inyección de Adversarios (Plan Experimental)

| Vector de Ataque | Perturbación Inyectada | Resultado Esperado | Detección Criptográfica |
| --- | --- | --- | --- |
| **1. Model Substitution** | Sustituir modelo declarado por un LLM local sin aviso. | $H_M'$ distorsiona $H_{12}$. | **Fallo en comprobación $TraceRoot$ ($100\%$)** |
| **2. Policy Tampering** | Desactivar *system guardrails* en tiempo de ejecución. | $H_P'$ distorsiona $H_{12}$. | **Fallo en comprobación $TraceRoot$ ($100\%$)** |
| **3. Input Tampering** | Modificar el prompt original antes del procesamiento. | $H_I'$ distorsiona $H_{345}$. | **Fallo en comprobación $TraceRoot$ ($100\%$)** |
| **4. Tool Hijacking** | Reemplazar binario de API/Tool por versión alterada. | $H_T'$ distorsiona $H_{45}$. | **Fallo en comprobación $TraceRoot$ ($100\%$)** |
| **5. Output Tampering** | Inyectar un payload JSON modificado post-inferencia. | $H_O'$ distorsiona $H_{45}$. | **Fallo en comprobación $TraceRoot$ ($100\%$)** |
| **6. Replay Attack** | Enviar un $TraceRoot$ previo para autorizar una nueva acción. | Bloqueo por `timestamp` y duplicidad de clave $key$. | **Rechazo inmediato en Smart Contract** |

## Estructura de Datos JSON (extracto relevante al riesgo)

```json
{
  "risk_score": 0.82,
  "verification_level": "ON_CHAIN_ANCHOR"
}
```
