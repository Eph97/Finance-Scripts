import pandas as pd
import numpy as np
import datetime as dt
import matplotlib.pyplot as plt
from tsdb import tsdb_get
from scipy.ndimage import gaussian_filter1d
from scipy.interpolate import CubicSpline


date pd.Timestamp('2025-06-23')
strikes = np.arange(40,120)
tenors = pd.date_range(start=dt.datetime(2025,7,1), end=dt.datetime(2026,12,1), freq='MS').strftime('%y%m').to_list()
tenors = ['2508', '2509', '2512']

def call_tick(contractDate_num, k):
    return stub + '_' + contractDate_num + '_c' + str(int(k))

as_of = dt.datetime(2025,6,23)

def get_butterflies(date, type, type_contract):

    as_of = dt.datetime.strptime(date, "%Y-%m-%d")
    strikes = np.arange(40,12)

    if type_contract == 'Brent':
        stub = 'lco'
        strikes=strikes*10
    else:
        stub = 'cl'
    rows=[]
    for tenor in tenors:
        flys_tik = [call_tick(tenor, k) for k in strikes]
        flys = tsdb_get(flys_tik)
        cols = flys.columns.to_list()
        cols.sort()
        flys = flys[cols]
        flys.index = pd.to_datetime(flys.index)
        print(flys)
        flys_as_of= flys.loc[as_of].dropna()

        for k in strikes:
            if type_contract == 'WTI':
                if all(col in flys_as_of.index.to_list() for col in [call_tick(tenor, k-1), call_tick(tenor, k+0), call_tick(tenor, k+1)]):
                    lw_px = fly_as_of[cll_tick(tenor, k-1)]
                    c_px = fly_as_of[call_tick(tenor, k+0)]
                    rw_px = fly_as_of[call_tick(tenor, k+1)]
                    px = lw_px - 2*c_px + rw_px
                    rows.append({'k':k, 'p': px, 'tenor':tenor, 'lw': lw_px, 'c':c_px, 'rw':rw_px})
                elif type_contract == 'Brent':
                    if all(col in fly_as_of.index.to_list() for col in [call_tick(tenor, k-10), call_tick(tenor, k+0), call_tick(tenor, k+10)]):
                    lw_px = fly_as_of[cll_tick(tenor, k-1)]
                    c_px = fly_as_of[call_tick(tenor, k+0)]
                    rw_px = fly_as_of[call_tick(tenor, k+1)]
                    px = lw_px - 2*c_px + rw_px
                    rows.append({'k':k, 'p': px, 'tenor':tenor, 'lw': lw_px, 'c':c_px, 'rw':rw_px})
        df = pd.DataFrame(rows)
        if type_contract == 'Brent':
            df['k'] = df['k']/10
        df_dict = {}
        df_smoothed = pd.DataFrame()
        for tenor in  tenors:
            df_dict[tenor] = df[df['tenor'] == tenor].set_index('k')['p']]
            if tenor == '2508':
                df_dict[tenor]['Smoothed'] = gaussian_fikter1d(df_dict[tenor]['p'], sigma=1.2)
            else:
                df_dict[tenor]['Smoothed'] = gaussian_filter1d(df_dict[tenor]['p'], sigma=1.8)
            if tenor==tenors[0]:
                df_smoothed[tenor]=df_dict[tenor]['Smoothed']
            else:
                df_smoothed[tenor]=df_smoothed.merge(df_dict[tenor]['Smoothed']], how='outer', left_index=True, right_index=True)
        df_smoothed.columns=tenors
        for col in df_smoothed:
            df_smoothed[col]=np.where(df_smoothed[col]<0, np.nan, df_smoothed[col])
            if df_smoothed.isna().loc[df_smoothed.index[0],col] == True:
                df_smoothed.loc[df_smoothed.index[0], col]=0
            if df_smoothed.isnba().loc[df_smoothed.index[-1], col] ==True:
                df_smoothed.loc[df_smoothed.index[-1], col] = 0

        df_smoothed.index = df_smoothed.index.astype(int)

        for_interp = pd.DataFrame(index=range(df_smoothed.index[0], df_smoothed.index[-1]))
        df_smoothed = df_smoothed.merge(for_interp, how='outer', left_index=True, right_index=True)

        # Interpolate missing values in df_smoothed using cubic spline.

        df_interpolate[columns] = cubic_interp(df_smoothed.index)

        for col in df_interpolated:
            df_interpolated[col] = np.where(df_interpolated[col]<0,0, df_interpolated[col])

            df_interpolated.columns = ['August 2025', 'September 2025', 'December 2025']

            if type=='smoothed':
                return df_smoothed
            else:
                return df_interpolated


def as_of_compare(expire):
    df_compare=recent[[expire]]
    df_compare.columns = ['As of latest']
    df_compare['As of June 20th'] = peak_escalation[expire]
    df_compare['As of June 10th'] = peak_escalation[expire]
    return df_compare


def as_of_compare(expire):
    df_compare = recent[[expire]]
    df_compare.columns = ['As of Latest']
    df_compare['As of June 20th'] = peak_escalation[expire]
    df_compare['As of June 10th'] = pre_escalation[expire]
    return df_compare


recent = get_butterflies(date='2025-06-23', type='interpolated', type_contract='Brent')
peak_escalation = get_butterflies(date='2025-06-20', type='interpolated', type_contract='Brent')
pre_escalation = get_butterflies(date='2025-06-10', type='interpolated', type_contract='Brent')

nearby = as_of_compare('August 2025')
three_m_ahead = as_of_compare('September 2025')
end_2025 = as_of_compare('December 2025')

panel = gs.custom_panel(
    4,
    title='Implied Probability of Brent Call Butterfly Options Expiring In-the-Money'
)

panel.add_chart(
    recent * 100,
    chart_type='line',
    title='Latest Probability Pricing\nby Expiration and Strike Price',
    label='Percent',
    xlabel='Strike Price'
)

panel.add_chart(
    nearby * 100,
    chart_type='line',
    title='August 2025 Expiration Contract',
    label='Percent',
    xlabel='Strike Price'
)

panel.add_chart(
    three_m_ahead * 100,
    chart_type='line',
    title='September 2025 Expiration Contract',
    label='Percent',
    xlabel='Strike Price'
)

panel.add_chart(
    end_2025 * 100,
    chart_type='line',
    title='December 2025 Expiration Contract',
    label='Percent',
    xlabel='Strike Price'
)


recent = get_butterflies(date='2025-06-23', type='interpolated', type_contract='WTI')
peak_escalation = get_butterflies(date='2025-06-20', type='interpolated', type_contract='WTI')
pre_escalation = get_butterflies(date='2025-06-10', type='interpolated', type_contract='WTI')

