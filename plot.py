import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import savefig
import matplotlib
import sys

RESULTS_FOLDER = './baselines/'
os.system('cp test_results/* baselines/')
if len(sys.argv) > 1:
    RESULTS_FOLDER = sys.argv[1]
NUM_BINS = 1000
BITS_IN_BYTE = 8.0
MILLISEC_IN_SEC = 1000.0
M_IN_B = 1000000.0
VIDEO_LEN = 48
VIDEO_BIT_RATE = [300, 750, 1200, 1850, 2850, 4300]
K_IN_M = 1000.0
REBUF_P = 4.3
SMOOTH_P = 1

SCHEMES = ['sim_cmc', 'sim_rl']
labels = ['Comyco', 'Pensieve']
LW = 2.5


def main():
    time_all = {}
    bit_rate_all = {}
    buff_all = {}
    bw_all = {}
    raw_reward_all = {}

    for scheme in SCHEMES:
        time_all[scheme] = {}
        raw_reward_all[scheme] = {}
        bit_rate_all[scheme] = {}
        buff_all[scheme] = {}
        bw_all[scheme] = {}

    log_files = os.listdir(RESULTS_FOLDER)
    for log_file in log_files:

        time_ms = []
        bit_rate = []
        buff = []
        bw = []
        reward = []

        # print(log_file)

        with open(RESULTS_FOLDER + log_file, 'r') as f:
            for line in f:
                parse = line.split()
                if len(parse) <= 1:
                    break
                time_ms.append(float(parse[0]))
                bit_rate.append(float(parse[1]))
                buff.append(float(parse[2]))
                bw.append(float(parse[4]) / float(parse[5])
                          * BITS_IN_BYTE * MILLISEC_IN_SEC / M_IN_B)
                reward.append(float(parse[-1]))

        for scheme in SCHEMES:
            if scheme in log_file:
                time_all[scheme][log_file[len(
                    'log_' + str(scheme) + '_'):]] = time_ms
                bit_rate_all[scheme][log_file[len(
                    'log_' + str(scheme) + '_'):]] = bit_rate
                buff_all[scheme][log_file[len(
                    'log_' + str(scheme) + '_'):]] = buff
                bw_all[scheme][log_file[len('log_' + str(scheme) + '_'):]] = bw
                raw_reward_all[scheme][log_file[len(
                    'log_' + str(scheme) + '_'):]] = reward  # np.clip(reward, 0., 100.)
                break

    # ---- ---- ---- ----
    # Reward records
    # ---- ---- ---- ----

    log_file_all = []
    reward_all = {}
    for scheme in SCHEMES:
        reward_all[scheme] = []

    for l in time_all[SCHEMES[0]]:
        schemes_check = True
        for scheme in SCHEMES:
            if l not in time_all[scheme] or len(time_all[scheme][l]) < VIDEO_LEN:
                print(scheme, l)
                schemes_check = False
                break
        if schemes_check:
            log_file_all.append(l)
            for scheme in SCHEMES:
                reward_all[scheme].append(
                    np.mean(raw_reward_all[scheme][l][1:VIDEO_LEN]))

    mean_rewards = {}
    for scheme in SCHEMES:
        mean_rewards[scheme] = np.mean(reward_all[scheme])

    SCHEMES_REW = []
    for scheme in SCHEMES:
        SCHEMES_REW.append(scheme + ': ' + str(mean_rewards[scheme]))

    # ---- ---- ---- ----
    # CDF
    # ---- ---- ---- ----

    plt.rcParams['axes.labelsize'] = 16
    font = {'size': 16}
    matplotlib.rc('font', **font)
    matplotlib.rc('text', usetex=True)
    fig, ax = plt.subplots(figsize=(4.5, 3))
    plt.subplots_adjust(left=0.17, bottom=0.19, right=0.97, top=0.96)

    lines = ['-', '-.', '-.', '--', '--']

    # colors = ['red', 'blue', 'orange', 'green', 'black']

    def rgb_to_hex(rr, gg, bb):
        rgb = (rr, gg, bb)
        return '#%02x%02x%02x' % rgb

    colors = [rgb_to_hex(68, 166, 69), rgb_to_hex(47, 103, 223), rgb_to_hex(239, 117, 38), rgb_to_hex(
        121, 90, 158), rgb_to_hex(34, 34, 34), rgb_to_hex(237, 65, 29)]

    for (scheme, color, line, label) in zip(SCHEMES, colors, lines, labels):
        values, base = np.histogram(reward_all[scheme], bins=NUM_BINS)
        cumulative = np.cumsum(values)
        cumulative = cumulative / np.max(cumulative)
        ax.plot(base[:-1], cumulative, line, color=color, lw=LW, label=label)

    ax.legend(framealpha=1,
              frameon=False, fontsize=16)
    # ax.spines['right'].set_visible(False)
    # ax.spines['top'].set_visible(False)
    plt.ylim(0., 1.)
    plt.xlim(-0.1, 2.5)
    plt.ylabel('CDF')
    plt.xlabel('Average QoE')
    os.makedirs('imgs', exist_ok=True)
    savefig('imgs/cdf_batch2048.png')
    print(SCHEMES_REW)


if __name__ == '__main__':
    main()
