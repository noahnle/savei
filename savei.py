import tkinter as tk
from tkinter import *
from tkinter import ttk

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageTk


def math():  # computing
    # get input values
    gas = gas_input.get()   # gas type options
    rho = float(rho_input.get())  # particle density
    To_C = float(To_input.get())  # gas temperature
    ER = float(ER_input.get())  # expansion ratio
    Tm_C = float(Tm_input.get())  # melting temp
    dp = float(dp_input.get())  # particle size
    Lex = float(Lex_input.get())  # expansion region length
    Po = float(Po_input.get())  # gas pressure
    Cp = float(Cp_input.get())  # particle specific heat
    uts_Pa = float(uts_input.get())  # tensile strength

    dp_min = dp * 0.9  # particle size +-10%
    dp_max = dp * 1.1
    To = To_C + 273.15  # c to k
    Tm = Tm_C + 273.15
    uts = uts_Pa * 1000000  # pa to mpa
    k_min = 0.5  # assume fitting parameter range
    k_max = 0.7
    k = (k_min + k_max) / 2  # best line of fit
    CVR_min = 1.5  # ~range for erosive effects
    CVR_max = 3
    CVR = (CVR_min + CVR_max) / 2

    # generate temp and pressure range
    K = np.linspace(20+273.15, Tm,  1000)  # in kelvin
    P = np.linspace(5, 70, 1000)
    d = np.linspace(5, 100, 1000)

    # call n define equations based on gas type
    if gas == 'Helium':
        def v_he(dp, rho, ER, Lex, Po, To):  # particle impact velocity
            eq1 = -389.3 + 91760.3 * ((dp * rho) ** -0.402) + \
                4.133 * Po + 0.357 * To - 0.00282 * rho + 1653 * Lex - \
                12.85 * ER + 0.0056 * Po * dp - 0.00257 * To * dp
            return eq1
        v = v_he(dp, rho, ER, Lex, Po, To)  # prediction
        trend = [v_he(dp, rho, ER, Lex, Po, To) for To in K]  # trendline plot1
        trend2 = [v_he(dp, rho, ER, Lex, Po, To)
                  for Po in P]  # trendline plot2
        trend3 = [v_he(dp, rho, ER, Lex, Po, To)for dp in d]  # trendline plot3
        plt.subplot(1, 3, 1)
        plt.fill_between(K - 273.15, [v_he(dp_min, rho, ER, Lex, Po, To) for To in K],
                         [v_he(dp_max, rho, ER, Lex, Po, To) for To in K],
                         alpha=0.2)  # plot1 range of error
        plt.subplot(1, 3, 2)
        plt.fill_between(P, [v_he(dp_min, rho, ER, Lex, Po, To) for Po in P],
                         [v_he(dp_max, rho, ER, Lex, Po, To) for Po in P],
                         alpha=0.2)  # plot2 range of error
        plt.subplot(1, 3, 3)
        plt.fill_between(d, [v_he(dp_min, rho, ER, Lex, Po, To) for dp_min in d],
                         [v_he(dp_max, rho, ER, Lex, Po, To) for dp_max in d],
                         alpha=0.2)  # plot3 range of error

        def Tp_he(dp, rho, ER, Lex, Po, To, Cp):  # particle impact temp
            eq2 = -103.29 - 858.46 * ((rho / dp ** 3) ** -0.151) + 337.7 * \
                ((rho / dp ** 3) ** -0.302) - 68.93 * ((rho / dp ** 3) ** -0.453) + \
                0.019 * Po + 0.577 * To - 494.4 * Lex - 3.998 * ER + \
                61.996 * ((Cp * dp ** 3) ** 0.1522)
            return eq2

        def vcr_he(k, Cp, Tm, Tp_he, uts, rho):  # critical impact velocity
            eq3 = k * np.sqrt(Cp * (Tm - Tp_he) + 16 *
                              (uts / rho) * ((Tm - Tp_he) / (Tm - 293)))
            return eq3
        vcr = vcr_he(k, Cp, Tm, Tp_he(dp, rho, ER, Lex,
                                      Po, To, Cp), uts, rho)  # prediction
        trend_cr = [vcr_he(k, Cp, Tm, Tp_he(
            dp, rho, ER, Lex, Po, To, Cp), uts, rho) for To in K]  # trendline plot1
        trend_cr2 = [vcr_he(k, Cp, Tm, Tp_he(
            dp, rho, ER, Lex, Po, To, Cp), uts, rho) for Po in P]  # trendline plot2
        trend_cr3 = [vcr_he(k, Cp, Tm, Tp_he(
            dp, rho, ER, Lex, Po, To, Cp), uts, rho) for dp in d]  # trendline plot3
        plt.subplot(1, 3, 1)
        plt.fill_between(K - 273.15,
                         [vcr_he(k_min, Cp, Tm, Tp_he(dp, rho, ER, Lex,
                                 Po, To, Cp), uts, rho) for To in K],
                         [vcr_he(k_max, Cp, Tm, Tp_he(dp, rho, ER, Lex,
                                 Po, To, Cp), uts, rho) for To in K],
                         alpha=0.2)  # plot1 range of error
        plt.subplot(1, 3, 2)
        plt.fill_between(P,
                         [vcr_he(k_min, Cp, Tm, Tp_he(dp_min, rho, ER, Lex,
                                 Po, To, Cp), uts, rho) for Po in P],
                         [vcr_he(k_max, Cp, Tm, Tp_he(dp_max, rho, ER, Lex,
                                 Po, To, Cp), uts, rho) for Po in P],
                         alpha=0.2)  # plot2 range of error
        plt.subplot(1, 3, 3)
        plt.fill_between(d,
                         [vcr_he(k_min, Cp, Tm, Tp_he(dp_min, rho, ER, Lex,
                                 Po, To, Cp), uts, rho) for dp_min in d],
                         [vcr_he(k_max, Cp, Tm, Tp_he(dp_max, rho, ER, Lex,
                                 Po, To, Cp), uts, rho) for dp_max in d],
                         alpha=0.2)  # plot3 range of error

        def ver_he(CVR, vcr):  # erosion impact velocity
            eq4 = CVR * vcr  # CVR = v/vcr -- critical velocity ratio
            return eq4
        ver = ver_he(CVR, vcr_he(k, Cp, Tm, Tp_he(
            dp, rho, ER, Lex, Po, To, Cp), uts, rho))  # prediction
        trend_er = [ver_he(CVR, vcr_he(k, Cp, Tm, Tp_he(
            dp, rho, ER, Lex, Po, To, Cp), uts, rho)) for To in K]  # trendline plot1
        trend_er2 = [ver_he(CVR, vcr_he(k, Cp, Tm, Tp_he(
            dp, rho, ER, Lex, Po, To, Cp), uts, rho)) for Po in P]  # trendline plot1
        trend_er3 = [ver_he(CVR, vcr_he(k, Cp, Tm, Tp_he(
            dp, rho, ER, Lex, Po, To, Cp), uts, rho)) for dp in d]  # trendline plot3
        plt.subplot(1, 3, 1)
        plt.fill_between(K - 273.15,
                         [ver_he(CVR_min, vcr_he(k, Cp, Tm, Tp_he(
                             dp, rho, ER, Lex, Po, To, Cp), uts, rho)) for To in K],
                         [ver_he(CVR_max, vcr_he(k, Cp, Tm, Tp_he(
                             dp, rho, ER, Lex, Po, To, Cp), uts, rho)) for To in K],
                         alpha=0.2)  # plot1 range of error
        plt.subplot(1, 3, 2)
        plt.fill_between(P,
                         [ver_he(CVR_min, vcr_he(k, Cp, Tm, Tp_he(
                             dp, rho, ER, Lex, Po, To, Cp), uts, rho)) for Po in P],
                         [ver_he(CVR_max, vcr_he(k, Cp, Tm, Tp_he(
                             dp, rho, ER, Lex, Po, To, Cp), uts, rho)) for Po in P],
                         alpha=0.2)  # plot2 range of error
        plt.subplot(1, 3, 3)
        plt.fill_between(d,
                         [ver_he(CVR_min, vcr_he(k, Cp, Tm, Tp_he(
                             dp_min, rho, ER, Lex, Po, To, Cp), uts, rho)) for dp_min in d],
                         [ver_he(CVR_max, vcr_he(k, Cp, Tm, Tp_he(
                             dp_max, rho, ER, Lex, Po, To, Cp), uts, rho)) for dp_max in d],
                         alpha=0.2)  # plot3 range of error

    elif gas == 'Nitrogen':
        def v_n(dp, rho, ER, Lex, Po, To):
            eq1 = -713.4 + 30661 * ((dp * rho) ** -0.264) - \
                190739 * ((dp * rho) ** -0.528) + 1.15 * Po + 0.254 * To + \
                0.003 * rho + 800 * Lex - 4.65 * ER + 0.019 * dp * Po - \
                0.0011 * dp * To
            return eq1
        v = v_n(dp, rho, ER, Lex, Po, To)
        trend = [v_n(dp, rho, ER, Lex, Po, To) for To in K]
        trend2 = [v_n(dp, rho, ER, Lex, Po, To) for Po in P]
        trend3 = [v_n(dp, rho, ER, Lex, Po, To) for dp in d]
        plt.subplot(1, 3, 1)
        plt.fill_between(K - 273.15, [v_n(dp_min, rho, ER, Lex, Po, To) for To in K],
                         [v_n(dp_max, rho, ER, Lex, Po, To) for To in K], alpha=0.2)
        plt.subplot(1, 3, 2)
        plt.fill_between(P, [v_n(dp_min, rho, ER, Lex, Po, To) for Po in P],
                         [v_n(dp_max, rho, ER, Lex, Po, To) for Po in P], alpha=0.2)
        plt.subplot(1, 3, 3)
        plt.fill_between(d, [v_n(dp_min, rho, ER, Lex, Po, To) for dp_min in d],
                         [v_n(dp_max, rho, ER, Lex, Po, To) for dp_max in d], alpha=0.2)

        def Tp_n(dp, rho, ER, Lex, Po, To, Cp):
            eq2 = 75.4 + 5.368 * np.log(dp) + 0.205 * To + 0.161 * To * np.log(dp) - \
                0.071 * Po - 0.0057 * rho - 307.7 * Lex - 2.04 * ER
            return eq2

        def vcr_n(k, Cp, Tm, Tp_n, uts, rho):
            eq3 = k * np.sqrt(Cp * (Tm - Tp_n) + 16 *
                              (uts / rho) * ((Tm - Tp_n) / (Tm - 293)))
            return eq3
        vcr = vcr_n(k, Cp, Tm, Tp_n(dp, rho, ER, Lex, Po, To, Cp), uts, rho)
        trend_cr = [vcr_n(k, Cp, Tm, Tp_n(dp, rho, ER, Lex,
                                          Po, To, Cp), uts, rho) for To in K]
        trend_cr2 = [vcr_n(k, Cp, Tm, Tp_n(
            dp, rho, ER, Lex, Po, To, Cp), uts, rho) for Po in P]
        trend_cr3 = [vcr_n(k, Cp, Tm, Tp_n(
            dp, rho, ER, Lex, Po, To, Cp), uts, rho) for dp in d]
        plt.subplot(1, 3, 1)
        plt.fill_between(K - 273.15,
                         [vcr_n(k_min, Cp, Tm, Tp_n(dp, rho, ER, Lex,
                                                    Po, To, Cp), uts, rho) for To in K],
                         [vcr_n(k_max, Cp, Tm, Tp_n(dp, rho, ER, Lex,
                                                    Po, To, Cp), uts, rho) for To in K],
                         alpha=0.2)
        plt.subplot(1, 3, 2)
        plt.fill_between(P,
                         [vcr_n(k_min, Cp, Tm, Tp_n(dp_min, rho, ER, Lex,
                                                    Po, To, Cp), uts, rho) for Po in P],
                         [vcr_n(k_max, Cp, Tm, Tp_n(dp_max, rho, ER, Lex,
                                                    Po, To, Cp), uts, rho) for Po in P],
                         alpha=0.2)
        plt.subplot(1, 3, 3)
        plt.fill_between(d,
                         [vcr_n(k_min, Cp, Tm, Tp_n(dp_min, rho, ER, Lex,
                                                    Po, To, Cp), uts, rho) for dp_min in d],
                         [vcr_n(k_max, Cp, Tm, Tp_n(dp_max, rho, ER, Lex,
                                                    Po, To, Cp), uts, rho) for dp_max in d],
                         alpha=0.2)

        def ver_n(CVR, vcr):
            eq4 = CVR * vcr
            return eq4
        ver = ver_n(CVR, vcr_n(k, Cp, Tm, Tp_n(
            dp, rho, ER, Lex, Po, To, Cp), uts, rho))
        trend_er = [ver_n(CVR, vcr_n(k, Cp, Tm, Tp_n(
            dp, rho, ER, Lex, Po, To, Cp), uts, rho)) for To in K]
        trend_er2 = [ver_n(CVR, vcr_n(k, Cp, Tm, Tp_n(
            dp, rho, ER, Lex, Po, To, Cp), uts, rho)) for Po in P]
        trend_er3 = [ver_n(CVR, vcr_n(k, Cp, Tm, Tp_n(
            dp, rho, ER, Lex, Po, To, Cp), uts, rho)) for dp in d]
        plt.subplot(1, 3, 1)
        plt.fill_between(K - 273.15,
                         [ver_n(CVR_min, vcr_n(k, Cp, Tm, Tp_n(
                             dp, rho, ER, Lex, Po, To, Cp), uts, rho)) for To in K],
                         [ver_n(CVR_max, vcr_n(k, Cp, Tm, Tp_n(
                             dp, rho, ER, Lex, Po, To, Cp), uts, rho)) for To in K],
                         alpha=0.2)
        plt.subplot(1, 3, 2)
        plt.fill_between(P,
                         [ver_n(CVR_min, vcr_n(k, Cp, Tm, Tp_n(
                             dp, rho, ER, Lex, Po, To, Cp), uts, rho)) for Po in P],
                         [ver_n(CVR_max, vcr_n(k, Cp, Tm, Tp_n(
                             dp, rho, ER, Lex, Po, To, Cp), uts, rho)) for Po in P],
                         alpha=0.2)  # plot2 range of error
        plt.subplot(1, 3, 3)
        plt.fill_between(d,
                         [ver_n(CVR_min, vcr_n(k, Cp, Tm, Tp_n(
                             dp_min, rho, ER, Lex, Po, To, Cp), uts, rho)) for dp_min in d],
                         [ver_n(CVR_max, vcr_n(k, Cp, Tm, Tp_n(
                             dp_max, rho, ER, Lex, Po, To, Cp), uts, rho)) for dp_max in d],
                         alpha=0.2)  # plot3 range of error

    else:
        v_result.config(text="Error: select process gas", fg='red',
                        cursor='pirate', font=("Calibri", 22))
        return

    # results
    vcr_label = tk.Label(window, text="Critical Velocity",
                         bg='#efc700', fg='black')
    vcr_label.grid(row=18, column=0, sticky='ew')
    vcr_result.config(text=f"{vcr:.2f} m/s",
                      bg='#efc700', fg='black')  # critical velocity

    ver_label = tk.Label(window, text="Erosion Velocity",
                         bg='#ff7575', fg='black')
    ver_label.grid(row=18, column=1, sticky='ew')
    ver_result.config(text=f"{ver:.2f} m/s",
                      bg='#ff7575', fg='black')  # erosion velocity

    v_label = tk.Label(window, text="Particle Impact Velocity",
                       bg='#00b102', fg='black', cursor='heart')
    v_label.grid(row=20, column=0, columnspan=2, sticky='ew')
    v_result.config(text=f"{v:.2f} m/s", bg='#00b102', fg='black', font=("Calibri", 26, "bold"),
                    cursor='heart')  # predicted velocity

    # convert trend values to a list
    trendline = list(trend)
    trendline2 = list(trend2)
    trendline3 = list(trend3)
    trendline_cr = list(trend_cr)
    trendline_cr2 = list(trend_cr2)
    trendline_cr3 = list(trend_cr3)
    trendline_er = list(trend_er)
    trendline_er2 = list(trend_er2)
    trendline_er3 = list(trend_er3)

    # plot predictions
    plt.subplot(1, 3, 1)  # v vs t
    C = K-273.15  # plot x-axis
    plt.plot(C, trendline)  # impact trend
    plt.plot(To_C, v, 'ro')  # predicted point
    plt.annotate(f'{v:.0f}', xy=(To_C, v), xycoords='data',
                 xytext=(0, 8), textcoords='offset points', ha='center')
    plt.plot(C, trendline_cr, '--')  # cr trend
    plt.plot(To_C, vcr, 'ro')  # critical point
    plt.annotate(f'{vcr:.0f}', xy=(To_C, vcr), xycoords='data',
                 xytext=(0, 8), textcoords='offset points', ha='center')
    plt.plot(C, trendline_er, '--')  # er trend
    plt.plot(To_C, ver, 'ro')  # erosion point
    plt.annotate(f'{ver:.0f}', xy=(To_C, ver), xycoords='data',
                 xytext=(0, 8), textcoords='offset points', ha='center')
    plt.title('Velocity-Temperature')
    plt.xlabel('Temperature (°C)')
    plt.ylabel('Velocity (m/s)')
    plt.grid(True)

    plt.subplot(1, 3, 2)  # v vs p
    plt.plot(P, trendline2)
    plt.plot(Po, v, 'ro')
    plt.annotate(f'{v:.0f}', xy=(Po, v), xycoords='data',
                 xytext=(0, 8), textcoords='offset points', ha='center')
    plt.plot(P, trendline_cr2, '--')
    plt.plot(Po, vcr, 'ro')
    plt.annotate(f'{vcr:.0f}', xy=(Po, vcr), xycoords='data',
                 xytext=(0, 8), textcoords='offset points', ha='center')
    plt.plot(P, trendline_er2, '--')
    plt.plot(Po, ver, 'ro')
    plt.annotate(f'{ver:.0f}', xy=(Po, ver), xycoords='data',
                 xytext=(0, 8), textcoords='offset points', ha='center')
    plt.title('Velocity-Pressure')
    plt.xlabel('Pressure (bar)')
    plt.grid(True)

    plt.subplot(1, 3, 3)  # v vs d
    plt.plot(d, trendline3,
             label=f'Impact; {To_C:.0f}°C; {Po:.0f} bar; {dp:.0f} µm')
    plt.plot(dp, v, 'ro')
    plt.annotate(f'{v:.0f}', xy=(dp, v), xycoords='data',
                 xytext=(0, 8), textcoords='offset points', ha='center')
    plt.plot(d, trendline_cr3, '--',
             label=f'Critical; {To_C:.0f}°C; {Po:.0f} bar; {dp:.0f} µm')  # cr trend
    plt.plot(dp, vcr, 'ro')
    plt.annotate(f'{vcr:.0f}', xy=(dp, vcr), xycoords='data',
                 xytext=(0, 8), textcoords='offset points', ha='center')
    plt.plot(d, trendline_er3, '--',
             label=f'Erosion; {To_C:.0f}°C; {Po:.0f} bar; {dp:.0f} µm')  # er trend
    plt.plot(dp, ver, 'ro')
    plt.annotate(f'{ver:.0f}', xy=(dp, ver), xycoords='data',
                 xytext=(0, 8), textcoords='offset points', ha='center')
    plt.title('Velocity-Size')
    plt.xlabel('Size (µm)')
    plt.legend()
    plt.grid(True)

    plt.suptitle('Particle Impact Velocity Analysis')
    plt.show()
    return


"""initiallize app"""
window = tk.Tk()
window.title("Savei")

# resizable window
window.minsize(694, 694)
window.maxsize(1920, 1080)

# window has two columns w equal weight
window.grid_columnconfigure(0, weight=1)
window.grid_columnconfigure(1, weight=1)

"""column 0"""
# gas type
gas_label = tk.Label(window, text="Process Gas")
gas_label.grid(row=1, column=0, padx=50, sticky='ew')
gas_options = ['Helium', 'Nitrogen']
gas_input = ttk.Combobox(window, width=16, values=gas_options, cursor='hand2')
gas_input.grid(row=2, column=0, padx=50, sticky='ew')

# particle size
dp_label = tk.Label(window, text="Particle Size [µm]", width=16)
dp_label.grid(row=4, column=0, padx=50, sticky='ew')
dp_input = tk.Entry(window, width=16)
dp_input.grid(row=5, column=0, padx=50, sticky='ew')

# density
rho_label = tk.Label(window, text="Particle Density [kg/m³]", width=16)
rho_label.grid(row=7, column=0, padx=50, sticky='ew')
rho_input = tk.Entry(window, width=16)
rho_input.grid(row=8, column=0, padx=50, sticky='ew')

# gas temperature
To_label = tk.Label(window, text="Heated Gas Temperature [°C]", width=16)
To_label.grid(row=10, column=0, padx=50, sticky='ew')
To_input = tk.Entry(window, width=16)
To_input.grid(row=11, column=0, padx=50, sticky='ew')

# melting temperature
Tm_label = tk.Label(
    window, text="Particle Melting Temperature [°C]", width=16)
Tm_label.grid(row=13, column=0, padx=50, sticky='ew')
Tm_input = tk.Entry(window, width=16)
Tm_input.grid(row=14, column=0, padx=50, sticky='ew')

"""column 1"""
# expansion area ratio
ER_label = tk.Label(window, text="Expansion Ratio", width=16)
ER_label.grid(row=1, column=1, padx=50, sticky='ew')
ER_input = tk.Entry(window, width=16)
ER_input.grid(row=2, column=1, padx=50, sticky='ew')

# gas pressure
Po_label = tk.Label(window, text="Inlet Gas Pressure [bar]", width=16)
Po_label.grid(row=4, column=1, padx=50, sticky='ew')
Po_input = tk.Entry(window, width=16)
Po_input.grid(row=5, column=1, padx=50, sticky='ew')

# expansion region length
Lex_label = tk.Label(
    window, text="Expansion Region Length with Standoff [m]", width=16)
Lex_label.grid(row=7, column=1, padx=50, sticky='ew')
Lex_input = tk.Entry(window, width=16)
Lex_input.grid(row=8, column=1, padx=50, sticky='ew')

# tensile strength
uts_label = tk.Label(window, text="Particle Tensile Strength [MPa]")
uts_label.grid(row=10, column=1, padx=50, sticky='ew')
uts_input = tk.Entry(window, width=16)
uts_input.grid(row=11, column=1, padx=50, sticky='ew')

# specific heat
Cp_label = tk.Label(window, text="Particle Specific Heat [J/kg-K]")
Cp_label.grid(row=13, column=1, padx=50, sticky='ew')
Cp_input = tk.Entry(window, width=16)
Cp_input.grid(row=14, column=1, padx=50, sticky='ew')

""""middle column"""
# logo
logo_path = '/Users/noahle/Desktop/savei/logo.png'
logo_image = Image.open(logo_path)
resized_logo = logo_image.resize((150, 150))
logo = ImageTk.PhotoImage(resized_logo)
logo_label = tk.Label(window, image=logo)
window.rowconfigure(0, weight=6)  # configure the row to expand
# place in both columns n centered
logo_label.grid(row=0, column=0, columnspan=2, sticky='nsew')

# set window icon
window.tk.call('wm', 'iconphoto', window._w, logo)

# predictions
window.rowconfigure(16, weight=1)
button = tk.Button(window, text="Predict Velocity",
                   cursor='hand2', command=math)
button.grid(row=16, column=0, columnspan=2, padx=200, sticky='nsew')

window.rowconfigure(19, weight=1)
vcr_result = tk.Label(window, width=16, font=("Calibri", 18))
vcr_result.grid(row=19, column=0, sticky='nsew')

window.rowconfigure(19, weight=1)
ver_result = tk.Label(window, width=16, font=("Calibri", 18))
ver_result.grid(row=19, column=1, sticky='nsew')

window.rowconfigure(21, weight=2)
v_result = tk.Label(window, width=16, font=("Calibri", 26, "bold"))
v_result.grid(row=21, column=0, columnspan=2, sticky='nsew')


"""spaces"""
space1 = tk.Label(window)
space1.grid(row=3, column=0, columnspan=2, padx=50)

space2 = tk.Label(window)
space2.grid(row=6, column=0, columnspan=2, padx=50)

space3 = tk.Label(window)
space3.grid(row=9, column=0, columnspan=2, padx=50)

space4 = tk.Label(window)
space4.grid(row=12, column=0, columnspan=2, padx=50)

space5 = tk.Label(window)
space5.grid(row=15, column=0, columnspan=2, padx=50)

space6 = tk.Label(window)
space6.grid(row=17, column=0, columnspan=2, padx=50)

# run the main event loop
window.mainloop()
