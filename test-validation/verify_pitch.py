pv=228; n=5; cagr=0.091; fv=pv*(1+cagr)**n
print(f"MarketsandMarkets CAGR check: {pv}B * (1.091)^5 = {fv:.1f}B, source says 352B")
pv2=248; fv2=pv2*(1.138)**8
print(f"Fortune BI CAGR check: {pv2}B * (1.138)^8 = {fv2:.1f}B, source says 699B")
print(f"PANW EV/Revenue: {164/9.2:.1f}x")
print(f"CRWD EV/Revenue: {111/5:.1f}x")
print(f"Google/Wiz EV/ARR: {32/0.6:.0f}x")
print(f"CyberShield EV range (comps): ${0.8*16:.1f}B - ${0.8*25:.1f}B")
print(f"CyberShield EV range (deals): ${0.8*10:.1f}B - ${0.8*18:.1f}B")
print(f"CyberShield EV range (EBITDA): ${0.16*20:.1f}B - ${0.16*30:.1f}B")
