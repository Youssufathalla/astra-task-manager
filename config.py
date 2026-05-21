"""Configuration constants for the Astra task manager.

This file keeps colors, text, starting data, and table definitions in one place.
Changing values here changes the look or defaults of the app without touching the main logic.
"""

import os

# =============================================================================
# CONSTANTS
# =============================================================================

# Window
WINDOW_TITLE = "Astra"
WINDOW_SIZE = "1500x900"
MIN_WINDOW_SIZE = (1250, 800)
TK_SCALING = 1.22

# App branding
APP_TITLE = "ASTRA"
APP_SUBTITLE = "Plan smarter, prioritize faster, and finish what matters."

# Small embedded PNG logo. Keeping it inside the code avoids extra image-file dependencies.
LOGO_IMAGE_BASE64 = """iVBORw0KGgoAAAANSUhEUgAAADoAAAA6CAYAAADhu0ooAAAXYklEQVR42uWbeZBd1XXuf3vvc4ee1N3q1tBCwrIkkNCA3GCEQAbMLMCAICYQYXiIwSSGMNg4rlQmHDsvLldcL44d4/gZsBk8gW1sjBFYiGABYhBPSEIz3RparbHV4+07nHP23vljn3PuuS1VbPKqXl4qXXWr+96+95z97bXWt7619roCsPw3+PH+Ix8SQoAQ/zkrtmCt+eBr/n0tKoQEAdaY/y8sJKR0uH/P9fxuoEK4N1n3Ni+Xo2lSB3Wt7ahcPcJoEAINWOveb7HRpcFYoudgEdjYGywYIbDWorBYIbAIhLWI1JIsIIUAIdFhQDB0lNKhXsKR4Roj/C4r/7tAhZTJjk2YOZsT5p1O4/gOPJmlUiwTlMvYMMAYjTYWa93DWIsxBms1xlqwFmMsCIFJblvdAIxxGyRA2CpEa90aZLQ5IleHam5C1OUJy8OMbN/A4fVrj1nrBwIaf7CurYO5n7ie9vEnEB4+SunwIcojQwR+mTAM0TpAhxoT7ajRGm10BNS4m1sHyRoNwsW41jq5s3WBV7WitccsUwgQCKSUqFwdmfZJjJs9h+z4Jnat+gUD29YjpcIY/fsDFVJhjWb8/MV0fnIFzQOjVPb1cPTIAUaKI/iVMmEYoLXGaGc1aww2soKNQVrrXov+54xn8H2furq8A5sQTNrBoxCIPCR+HgOWUpGREmkFuY6pTL30Mnrfe4c9z34fqXIY7R8DSwEP1oL0HMjOj7N4xT209B6msr+Hvft2MTQySBgGhDFAYxxI6wDGburczlbBWgsCgiBg4oQ2liw5ky1b3yebzWK0TixorSU2rvMG6x7J69FzowmNBiWwxVH6N21kxtJliMnTGXxvHdLLunBIgZW1vKPAQG76Qk5fcTeNu3sp9O7l/d07qFRKGGvR2mCMRRsXd86C1rluHKPJTWxyM6UUhcIo191wHd956GtMnDgBPwgRUjlGr80gRNhq3Dm9cdYYQj+gHFSwJmDrww9x0tnnMOGCazEhCC+PSMGTVR+WCJXF5lpYcPu9NB4ZYmR3F7t6dmG0QYcarTVah5gwrFo0jkcTL8Q93P8cMQkpGC2WmDt3DjevuIn2liYeuO/TjBbLSM9zbBxxrY0tFz2xNQ9S3uKurUNNsVzChGW2P/4onTfegpw8E6tyILMJWBmFOqgMJrS0XngVHR1TGd3wLr2Hewn9CkHgE4SBA6cdYGtMBDAGp8f8rrqcEJJKJeDBv/wss6a2MTRa5o5bbqCz81QKo2WQMgESE5NNAYo9wxKzeezqVcLTQP/ObRS6djDjD2/GGoXI5kGkgCIUQmWhYQIzL/0E/qZNDPYfZrQwjNahs2RYjcsqEJOkEYuN4tXFqrGOgKRSDA2PcMklH+eiT1yGDg0NuQx1dXn+/HN/TKgNQimskBE3OusSu64guWbauiaO3wh4GATIjMeeF1cy/YwzoGMWqAzIDCCRAgFCYaxEnXwq7a2tDG/dykipgI5dVGuXK7XB6MgtrcYaXQUbWVgbnbIEhNrQUF/H3/zVA+Qygp09B1n73vsAXHvVJVxwwXkURisoz8MKqmCoJbn0NZN4JQ3eYAUM7+5Gjg7T9JFFGCNBZRFCIhHSIRcZmmfPQw32Uxrsx/fLaG2iXJl20aq7JPFoYzIyCRlZ69LA8NAQK269idM655G3lm98+zH++ZdrGCr6KKX46y/chaprwsgMVkhMQj5xjJpqCCSMnM63ohqvRhOWiozs7aZt9lyQOYSXwQqFBImQHng5GiZPoXzkMJVSET8I0LEVE8KJ/47iEJIcqnU6Zi1CCIrlCifPnsUXPncnEnji6V/x4spV5BqbWbl5L2A596xOrv2DqxgthqhMNrpmtIFUY9RtaC3Z2ThEkrTjnhcOHqRufAtk60AqQMUWdUA9KfFHhggC34kBk2ZQjTFhLdmYqigg2lWbUlaB73PHnbeRaWnlwMHDfO0bD9PW0cGsVo//s+sI7/f2AfCX991C/YQOQu3ESmwlopQ1VjXFqcfaWsKKGTscLaC0diClAimRCBUBzWD8CmHFdwQUVtOINW43TYppdSL1xhCUMUgpGRkucN45i7no8isYLmi+9JVvIBva0FR48qt/Qbtn+eU7XWitmT9rGrfdeDWVQhkpqyCtOQ4BJWx+bOqJra6DAF0cdUymPEhiVEinJIIKNgIZx1riqhGY2I1sLBCMqVVIQBhq8jmPm2+9hWy+npd+/Wve2LCTWQvns/2N1WzftpWet1fh5ep4feseAD5/+x/Q1jGRwA8Q6VyZSmEkFcpYkHFeJSkgTOCD1cT4qkCtAb+CNdoBjeOwJi5S2tZatDHoGvd21iwOD7Ns2RXMP+2jHOndw49+/jyX33gzG9aupjx0FCkljz70T2RH+1i/u4+R0RLTTpjEn9z6h4TDo0gpo3ukCoIox9aw7BjJSQqw1RqMTtxe2kgsYw1GB4TG1rhoHPBx8GtTBRW/ZlNxVCmXmTJ1MstvupGMJ/nBkz+icfKH2Ll7Jzt/+yuUVEihKAwd5alHv8O0iW2s3tAFwN13LGfyzOn45XJSA1crm6paSseuPca60Zp0DFLEMSpdZRBZtlpLVi1FKo3UEEDNLhqEgKBS5pprlzFxyjTWvbGWtzfvYtyJ03j2O/+IFAKLhzYKJTOsfu6nrFu7hnXdh9jVe4hJE9q4909uxpSLSClTbhqXe+nwsXHZk1JPbkkagdbRZkSGlCJ2XcBKdZwYqFqPYxJ41aJSCMrFIvPmn8IZHzuXA709/PQXKzn7qmt4fdVzBEd2I0QeYxTWKqzIIazm0X/6Gi15xUsbujFac/v/uJ4PzZ5NWC4hRZJQax7plGOrSRVrDQIwgI4qpqgARlabXAKkGuOSprZiSMWDidNJLBIsSCm5atnVtLa2snLli+jGNroO7KXrhadQMo+xClU/Dq+5DWMUSjVyoPs93nzpeQ4Mllnz7nba28Zz3913YMOKa8LZtEqogqq+Flk6qWYtGIOI3Ta2qHvicqn1MhhsJAgi65mx0it1k+iXFAJ/tMBZZy1i3sJOevd0s3PfUSYtOJVV3/0mEo2Veay11E2fQUvn6a5npHJImeeXTzzCyJH9vL5tP8VSmVtuuo6Z8xagKyWkTPUG7PEsnJJSqUxgY1xR28ZZVAiQHsbLud7OGG1JqnxKBHvKbbTWNDY3cfHSS7HW8PzKVbTPPZXXVr9IeHA7qCZsJK6bTpjGxAWdrtPq5RCqnkqhj9/89Ie0TWjjlQ3v09I8jvvvuROrg6qqj4EYU2vRNFdEazWAiUgobvDJdLlrtY5YVadUj+vkmYiM0gRgrUFICEslPn7+uZxw4nTeXLuWUq6ZfcVRun/1Q6RswMosIpMFsjR2TOHEhZ2QG4/I1aNVFuW18O6alaxfu4Z1u46w/0g/t918PbMXno6uRMQUMy3HVORp8QtYjJDobN55aeQJsurHFlupYLWNumm2RhwkMZvqtAkhCCs+k07o4OxzzmNooJ9tXXtpnbeQt37yODIsYr06yGQRuQZkpoH81Km0zp+HnHQSIj8OkcljvRxCKJ5+7HuMlH2efOFNvEyG+++5MyX/LMe2IY4DNn5JqMRtwSKJSiOMxgQ+2hgQqZqyJt3YlICOu34hF150Aa1tbby25lVkx3TeeuM1/K53wBuHVVlstgHdOBHTPIPRD58EM6dhOhYS2ixWZTHSQ2ab6evexOurVtIXZnht/XauvvIyPrL4rMiqiuMitbG2pibfWr8SKSk7psNgXdMpCehIayYVvWOmJIkLCUG5xEmzT+Kcc8+jZ/cudhwcoHt4mD3P/gCp6jBeFpmrJ98ygUmzFnLGinuZfuZHGdfqcdGFnUw/aS5N7VNRuUaMyiBVnjefeRxdGmbLkSKFUsCn77jVuaDrdx5jXaFcP9hURqO+ePSmSskpo8hjlcg0PCiyOSyShpmzyeuAQtcOtCCxZFWlkKgRtz2W5Z+6kfFtbbzx9nqYOY+Nz/4YMbQfm2kk19DEh89fypybP03nZz7FkuWdTJjUhCxrTlk6n/bLLmf8rHlkpWS0dzdBqYSuDNA3HHDiwkUUhgZZ1Dmft9ZvZH/3DlQ2l5wGICV4HrZcRBrD1KWXoZSidOQgdTPnYeubKW7f6HJx6EeHTHG1IGSiXa2VVa1pq9RuceIgKJY4Y8ki5i1YwKrf/IbB/Hj2dW3H7N+MVOOwCPzSKDtffpGd6zfBT+bCR86m8+4rCKaM571/+Fd4dRV0bYADO6E47PKdamLnmufYuugsplx6Kdu2bOeGG65n68YNlIuuv4RSWD8Ev0DH4rM54Z77OPjr5+hf/RJCulan0Do5HrHWRqxr4+ZyXAqZxP/Hti2IYjbf1MAnrriC/ft76Rko04di1wtPIUU26vm4LoPwi4j+XuTWdYiVb6F3DTFUClCvdqM2bULu74JyMTpziZrUhLz8o0cwQcDDu0u8rNponDIdpMBKhS2WaJw6jbnf/mcm/PAnbHvqZ+x74lsIoRyn6DDqMR/32NAijAETd9dTqYRqh05KSTha5KKLL6O1vY3Vr6yl/azz2fDEdxCVAZDjUkdMYKXnmLWxBSsKHOjaiZ5Qhx7ai2iqx5bqIaxE8eRSmVT1DPRu5eHvPYzf2saWH30P/AAqhuzEibTc/0eM+8xdDJQUBz75SXjnRWSmpVrBGIsNwxoy8qolTjVfVi1Zq0gEoH2fto6JfPyCC9i8eRuF5sn0dO2ktPVVlzPj0y0hI/vgQJSHYWArhZ1byExqga43QRYQQbm6IBGf+VikrOfdpx4BKoDCa5hK+2dWUHfXLYxOOZm9r+zAv+8GxO71CK/J5X2lXMZAYrVJAbV4jKnpEmVESvpFGlIIsGHA0qWXIISk+0A/lTmnsf1//TVCulThkMrqYXGUuvBLUPExPbvQm8fB8AGolxBGBXKiTaU7asBDmCJStZC5/CpmfPGzZOcsYN9uQf+T/4r50m3IQ91Y1eC8T8jI9SMuCUNSB3dUpUPS5NJR/hQ1rUUhQJcrfOikmSxesoTfvrKGcsd0tqx+DlU4ACaHNhWoG+eubW0Sq+gA4VswIaZnN1pY8Edc91H70bGhdMlOeFi/grAadfq52E8/gLr+Yop7B9m1epjSuy8gvnoXYrgPq+qc3qs5gY/umUqVY2LUYMOwNjbH6EghBcuWLWNgcJBtBwcZCA9ydM3PybdOpv6aWyhvXEdp3VqsyEJjg7Oqjm7qxCR6725M/1GQthqbcboILWiNmjUHcekfYc+/llxrM/KpLewWjfDmk8hH/garQ5B1YJwHWCGqKRbr3DYuvKP87zlQBqx0ggFbmzOtQUpBWCzxkUWnc+ppnTz2+I9hxhwO/OwRhFCUh0bx33yL+s//T1qGDuA//QjFdzZiAx/qc24ROnStqf6jiIEBhFJuEV4GQo0NAtTkDsTZS9Ezl5Btaid3ZJDy3iGKlRLipa/CC9/HCg9kHndqrKIT+bjDnzoH1REZRS96pNoTNlWLpjWmMeDlcyz/1I2se/sdBls6OLB1PfrILqRsBOVhNr9K4YFPkfv6M0z88TOMf3sNA088TfDb16iM9Du9K0CEfqLZLEAQIltaUactQX/4DEQpQ1tGYmZMZmhCB3bnBuTDn8VuXAMyC1a6hxCRJUVylCHGnL4lQC14xL1xY2tLoOhQRypFODrMZddcSy6X5fV3t2Knn0zfay+4nGkNhGXw8oi+Hvw/vZIDX3mMcVefw/hzzqG8YRuVx35K5eUXKB/e7ywopQPY2EhubifhtPkEI9DUN0TrJaczsGgx5SaP/DM/p/TFezFHexAqHy1VEbd/0iBrqrAk7AzROQcKlX9QqAwYS+aEmUjt4+/rwgiJwGBDTVNLC3fceTvvvPc+2ebxrPvFD9CFfuc6cQ62GrwstlSAl58naJtNuOAkxPh2yrPOpX7ZxTQ1tqD39WK0JXPKQjKLL6OcnwK7ejnxlElMfuBaDl40H2UCvL/7MqW//TNsafC4IF3hFZGQqNKrsAZv2iysyhLs3Y6QAqEDPBFbUBxb7gih0H6Bq6++HpXJQzbP60//b0qHu5Eyl3prdEMTIrwspjyM+Ku7CNXXCFZcQ+u0CoWByQzNvoLmez5Kdvs6igWBf2iY9roKU+67jt4Lz2T/eMns97rovfvPGX7l2WjEJue8Tahqx0CMtWJtfWqjc5jYotbaNBkJnAJ2MwhCWbRfob1jKtcsu5K1727nme9/i+G+HqT0kgMekvmC6hySUB7ajFL5s/vJ9/Uz8Le30eyVyedLHOnRcMhHHexh3hUfI1x+PpsnjUdaaHni1+z4iy/h793oCnWt3XVlRDZpd01YJ12vimQGQqS7EtbgWWPcrJAVyKg96PKmwIaj3LriPo4OjvIvX/8qw0f3oaSHMel+jKxxIyEkGIvAYLwKpX/4e+qLJfq+dDcNy+cy6/V9BMEBTrn3CrqXzKZLQEPfKPLvH+Lotx/ClPscSGNBZpLej0hg2JpUkmj1SMCLqCEgktYLDmiMGCvQ5RJePo9SikpxlDkLOpkx62S+8PnPRSAz0byQrKqY2JWEo3ubmiBBW2zGZ/RbX6epWCH4x/spnDOVuxdfS3dGEgCZ9d3s+cJXGH75WVA+wstEYySyOsw1tgFW20sZO1KDytVjiqUaoBKrXc4BgsE+TH0LVgiy+RxnLl7Ml7/8d/Qf2nUsyERfpf+m1srSDX+InGbk8e+S+9y3qC9bxmcEJ1soPvEKO667k8LLP0NkcTJSZkBlnWpSHsTDHBHpCCFIV1xQ+1wohWxoJuw/5DbBaEdQguiMQmUIj/QSzD2TMFPH1EmtrF69mn3dm1Ay66ZZUsfvcdO7Kr/iOaBqhx1jHOZQIDyfwUe/SVYKjv7p9fzwm0+y5dHvIsJ+RMM4tzGRLrbYqC+bsuBYlZa2aFIqGWRTKybfQHC4x210WAarUWAfFIBQGWylhJw4nUzGY2jHRgaP9kXEE4OMuvpCAXGFIlJHGimiQCa5WCRDGwGjm7fw8qYiR95+B+lpaGgHr87NGkh3vRoQNa5ajUlnWFvlICEgrFC/4GyEzFDZ+qZ7j64AoRuoEskHJFRKiHlnY7o3pW4kUrQuk1gQacaVMtGdbvjDnbsKLw+5RmhohQmzEWfdhLhwOfJDH8XoDFiNsBarfURiPdeZJW7l1MSmrU0sqXFamaunacmVjKxdiSkOI4wPNsCi3aotBoyPMCF6//vowz14ZyxFhGUXM8n5zFi3lZFlo0kSpBuQUp6LMS8H2XrIj4PmE2DSHGhowe7fh+nZBuXBpNVaTXNjDpGIe1Sp+liMmfCTChsWaTlvGf7enYQHu3AhWcGiaweqLCGEJYQN0W8/j2puJ3PapRAWQHrVhB3voKhaUAiZEIYD7UZ6UFnwso5UjIbCEejZiNjxFhzcBoVDUDwKQdHVpSZMyisRtVeFHatiq2M5bm8l1h+mcdFSVP04htf+ynmTLkcg7fGHHgUKhAfZepouv53w6H6Kv/25c5lMLtVLlSn5VXVdpKr+9vIObKYOcg3OhetbQeWwfhHhj2L9AqJcgErB1abax+rQuXEE2nUizZgmtcCGrnfb+LErqeuYTt8v/gUCF5PWhr/HGKsQCCtAZmi8eDlMmEJxzUr0nq1ACHhuODIiD5vuKERArVRu8ELlIJOvPrxoUkT7EJQhKIEO3N/aj8ornSqeLTaK43TvWSBRk0+k8axLkOUCAy88DiaIjmrMBxlMrv4r9+F5ZM68EKElYc9uwv170MODrt6sIXtnYSuq7CykF+VDzwFVWbchOnDuGlvQRADTnYGkxRL1kb0sor4Rr20SmakzEHV1BJtepdz9bpWYrP2PjprLZEgiO2kquemn4DU0I7TEBCFW2zHDxPGQU3WKuqqcoriOh4ej803XsXOyMf6cSAFMvCyXwWKwlQLBob0EB3cfs8b/uy8PxCw75mL/Gd+TsMekFvE7QX6gb0nUqqDjn2D9P/huRJUAP+D9PxjQ/8I//wabIoqJSLUXDwAAAABJRU5ErkJggg=="""

# Colors
APP_BG = "#020617"
PANEL_BG = "#0f172a"
CATEGORY_PANEL_BG = "#111827"
TABLE_BG = "#0b1220"
INPUT_BG = "#1e293b"
DISABLED_BG = "#111827"
DISABLED_BUTTON_BG = "#334155"

WHITE = "white"
TEXT_MUTED = "#94a3b8"
TEXT_LIGHT = "#cbd5e1"
TEXT_FADED = "#64748b"
TEXT_DARK = "#0f172a"

# Premium accent colors
# The interface still matches the Astra logo, but uses a broader range for better contrast.
CYAN = "#22d3ee"
CYAN_HOVER = "#06b6d4"
CYAN_DARK = "#0891b2"
CYAN_DARK_HOVER = "#0e7490"
SKY = "#38bdf8"
SKY_HOVER = "#0ea5e9"
TEAL = "#14b8a6"
TEAL_HOVER = "#0d9488"
EMERALD = "#22c55e"
EMERALD_HOVER = "#16a34a"
VIOLET = "#a78bfa"
VIOLET_HOVER = "#8b5cf6"
AMBER = "#f59e0b"
AMBER_HOVER = "#d97706"
ROSE = "#fb7185"
ROSE_HOVER = "#e11d48"
RED = "#ef4444"
RED_HOVER = "#dc2626"
SILVER = "#e2e8f0"
SILVER_MUTED = "#94a3b8"

# Supporting UI colors
BLUE = SKY_HOVER
BLUE_HOVER = "#0284c7"
GREEN = EMERALD
GREEN_BUTTON = EMERALD
GREEN_BUTTON_HOVER = EMERALD_HOVER
PURPLE = VIOLET_HOVER
PURPLE_HOVER = "#7c3aed"
LIGHT_PURPLE = VIOLET
ORANGE = AMBER
GRAY_BUTTON = "#475569"
GRAY_BUTTON_HOVER = "#64748b"
BORDER_GLOW = "#164e63"
SOFT_SHADOW = "#01040c"
HOVER_ROW_BG = "#102436"
SELECTED_ROW_BG = "#075985"
CONFIRM_CANCEL_BG = "#e2e8f0"
CONFIRM_CANCEL_HOVER = "#cbd5e1"
POPUP_BG = "#f8fafc"
POPUP_TEXT = "#334155"

# Starting data
STARTING_CATEGORIES = ["Uni", "Work", "Gym", "Personal", "Projects"]

MONTHS = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
]

STARTING_TASKS = [
    ("Finish Python task manager", "Projects", "High", "2026-05-20", "No time", "Pending"),
    ("Study PCAP OOP module", "Uni", "Medium", "2026-05-22", "02:00 PM", "Pending"),
    ("Push project to GitHub", "Projects", "High", "2026-05-21", "06:30 PM", "In Progress"),
    ("Gym session", "Gym", "Low", "2026-05-19", "08:00 PM", "Completed"),
    ("Review cybersecurity notes", "Personal", "Medium", "2026-05-24", "No time", "Pending"),
]

DASHBOARD_CARDS = [
    ("Total Tasks", "total", SKY),
    ("Completed", "completed", EMERALD),
    ("In Progress", "progress", VIOLET),
    ("Pending", "pending", AMBER),
    ("High Priority", "high_priority", RED),
]

ACTION_BUTTONS = [
    ("+ Add", BLUE, BLUE_HOVER, "add_task", False),
    ("✎ Update", GRAY_BUTTON, GRAY_BUTTON_HOVER, "update_selected_task", True),
    ("▶ Start", PURPLE, PURPLE_HOVER, "start_task", True),
    ("✓ Complete", GREEN_BUTTON, GREEN_BUTTON_HOVER, "mark_complete", True),
    ("🗑 Delete", RED, RED_HOVER, "delete_task", True),
]

TABLE_COLUMNS = (
    ("title", "Task", 360, 240, None),
    ("category", "Category", 135, 110, "center"),
    ("priority", "Priority", 115, 95, "center"),
    ("due_date", "Due Date", 135, 110, "center"),
    ("due_time", "Due Time", 125, 100, "center"),
    ("status", "Status", 135, 110, "center"),
)

TABLE_TAG_COLORS = {
    "Pending": "#fbbf24",
    "In Progress": VIOLET,
    "Completed": "#86efac",
    "Overdue": ROSE,
}

PRIORITY_RANK = {"High": 1, "Medium": 2, "Low": 3}
STATUS_RANK = {"Pending": 1, "In Progress": 2, "Completed": 3}


# =============================================================================
# SMALL HELPER FUNCTIONS
# =============================================================================

# =============================================================================
# FULL APP VERSION CONSTANTS
# =============================================================================

DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "astra_tasks.json")

ACTION_BUTTONS = [
    ("Add", BLUE, BLUE_HOVER, "add_task", False),
    ("Update", GRAY_BUTTON, GRAY_BUTTON_HOVER, "update_selected_task", True),
    ("Start", PURPLE, PURPLE_HOVER, "start_task", True),
    ("Complete", GREEN_BUTTON, GREEN_BUTTON_HOVER, "mark_complete", True),
    ("Notes", VIOLET, VIOLET_HOVER, "open_notes_popup", True),
    ("Delete", RED, RED_HOVER, "delete_task", True),
]

TABLE_COLUMNS = (
    ("title", "Task", 340, 230, "left"),
    ("category", "Category", 120, 100, "center"),
    ("priority", "Priority", 115, 95, "center"),
    ("due_date", "Due Date", 125, 105, "center"),
    ("due_state", "Due Status", 115, 95, "center"),
    ("due_time", "Due Time", 115, 95, "center"),
    ("status", "Status", 130, 110, "center"),
)

FILTER_DEFINITIONS = [
    ("All", "All"),
    ("Pending", "Pending"),
    ("In Progress", "In Progress"),
    ("Completed", "Completed"),
    ("High Priority", "High Priority"),
    ("Overdue", "Overdue"),
]

BADGE_COLORS = {
    "High": ("#3f1218", RED),
    "Medium": ("#3a2608", AMBER),
    "Low": ("#062f2a", TEAL),
    "Pending": ("#3a2608", AMBER),
    "In Progress": ("#2e1f5c", VIOLET),
    "Completed": ("#06351f", EMERALD),
    "Overdue": ("#3f1218", ROSE),
    "Today": ("#073447", CYAN),
    "Tomorrow": ("#3a2608", AMBER),
    "Upcoming": ("#102436", TEXT_LIGHT),
}

DUE_STATE_RANK = {"Overdue": 1, "Today": 2, "Tomorrow": 3, "Upcoming": 4}


# =============================================================================
# CUSTOM CANVAS TASK TABLE
