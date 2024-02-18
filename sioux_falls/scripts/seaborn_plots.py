import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import spearmanr

#10, 0.49411764705882344
#20, 0.8130718954248366
#30.061728395061735, 0.8862745098039215


def rank_corr(data):
    sns.set_theme(style="whitegrid")
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))

    for i, lmbd in enumerate(data):
        y = data[lmbd]['y']
        x = data[lmbd]['x']
        sns.scatterplot(ax=axes[i], x=x, y=y, color='black')
        corr = spearmanr(x, y)
        props = dict(boxstyle='round', facecolor='white', alpha=1.0)
        axes[i].text(
            100, 1700, rf'$\rho = {corr.correlation:.2f}$', fontsize='xx-large', bbox=props)
        sns.lineplot(ax=axes[i], x=range(len(x)),
                     y=range(len(y)), lw=2, color='black')

        axes[i].tick_params(axis='both', which='major', labelsize=20)

        axes[i].set_xlim(0, len(x))
        axes[i].set_ylim(0, len(y))
        if i != 1:
            axes[i].set_xlabel(f'$\lambda = {lmbd}$', fontsize=20)
        else:
            axes[i].set_xlabel(
                f'$\lambda = {lmbd}$\nSubnetwork vulnerability ranking', fontsize=20)

        if i == 0:
            axes[i].set_ylabel(
                'Full network\nvulnerability ranking', fontsize=20)

        #plt.xlabel('Subnetwork vulnerability ranking', fontsize=20)


def ga_plot(vul_dict, baseline=None):
    """
    args:
        vul_dict: Dictionary of vulnerabilities,
                  key is the label and value is a list of vuls
    """

    linestyle_tuple = [
        #('dotted',                (0, (1, 3, 1, 3))),
        ('densely dotted',        (0, (1, 1))),
        ('dashed',                (0, (5, 5))),
        ('dashdotted',            (0, (3, 3, 1, 3))),

        ('densely dashed',        (0, (5, 1))),

        ('densely dashdotted',    (0, (3, 1, 1, 1))),

        ('densely dashdotdotted', (0, (3, 1, 1, 1, 1, 1))),
        ('dashdotdotted',         (0, (3, 5, 1, 5, 1, 5))),

        ('loosely dotted',        (0, (1, 10))),
        ('loosely dashed',        (0, (5, 10))),
        ('loosely dashdotted',    (0, (3, 10, 1, 10))),
        ('loosely dashdotdotted', (0, (3, 10, 1, 10, 1, 10))), ]

    sns.set_theme(style="whitegrid")
    fig, axes = plt.subplots(1, 1, figsize=(14, 10))

    if baseline:
        y = [baseline for i in range(41)]
        print(baseline)
        sns.lineplot(ax=axes, x=[i for i in range(len(y))], y=y, lw=3,
                     label='B = 0 for $\\lambda$ = 3', color='black')

    for i, (label, vuls) in enumerate(vul_dict.items()):
        print(vuls[0], vuls[-1])
        sns.lineplot(ax=axes, x=range(len(vuls)), y=vuls,
                     lw=3, ls=linestyle_tuple[i][1], label=label, color='black')
    # sns.lineplot(ax=axes, x=range(len(avg_vul)), y=avg_vul,
    #             lw=2, label='$B = 15$ for $\lambda = 3$')
    # plt.hlines(y=1.357, xmin=0, xmax=40,
    # label='Full network vulnerability\nwithout VMS', color='red')
    # plt.hlines(y=2.334, xmin=0, xmax=40,
    # label='Network vulnerability w/o\n VMS for $\lambda = 3$', color='red')
    # plt.hlines(y=1.097, xmin=0, xmax=40,
    # label='Full network vulnerability with best VMS configuration')

    axes.tick_params(axis='both', which='major', labelsize=24)
    axes.set_xlabel('Generation', fontsize=24)
    axes.set_ylabel('Vulnerability', fontsize=24)
    plt.legend(prop={"size": 21}, loc='lower center',
               bbox_to_anchor=(.5, -.25), ncol=3)
    #plt.ylim(0.8, 2)
    plt.xlim(0, 40)
    # return fig


def corr_plot(x, corr, speedup):
    fig, ax1 = plt.subplots(figsize=(14, 10))

    color = 'black'
    ax1.set_xlabel('Subnetwork size ($\lambda$)', fontsize=24)
    ax1.set_ylabel("Spearman's Rank Correlation", color=color, fontsize=24)
    ax1.plot(x, corr, color=color, lw=4, label='Correlation')
    ax1.tick_params(axis='both', labelcolor=color, labelsize=24)

    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

    color = 'black'
    # we already handled the x-label with ax1
    ax2.set_ylabel('Speed up', color=color, fontsize=24)
    ax2.plot(x, speedup, color=color, lw=4, ls='dashed', label='Speed up')
    ax2.tick_params(axis='y', labelcolor=color, labelsize=24)

    fig.tight_layout()  # otherwise the right y-label is slightly clipped
    plt.xlim(1, x[-1])
    ax1.legend(prop={"size": 21}, loc='lower center',
               bbox_to_anchor=(.35, -.2), ncol=1)
    ax2.legend(prop={"size": 21}, loc='lower center',
               bbox_to_anchor=(.65, -.2), ncol=1)
    plt.show()
