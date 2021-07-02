import pandas as pd

df = pd.read_csv('my_outlay/Vpsk_69031392.csv', index_col=False, delimiter=';',  skiprows=25, skipfooter=10, encoding='cp1251',
    names=['date', 'operation_name', 'amount', 'currency', 'dateop', 'com', 'ob', 'card', 'category'])

#df.drop(['dateop', 'com', 'ob', 'card'], inplace=True, axis=1)

df['dateop'] = pd.to_datetime(df['dateop'], errors='coerce')
df = df.dropna(subset=['dateop'])

print(df)


'''df['amount'] = df['amount'].str.replace(',', '.')
df['amount'] = df['amount'].str.replace(' ', '')
df['amount'] = pd.to_numeric(df['amount'])
print(df.dtypes)
df['amount'] = df.query("~(amount < 0)")
print (df)
#df.loc[df.amount < 0.00000]
#print(df)

a = 1.2
if a > 0:
    print('True')
else:
    print('Это говно не работает')



*objects.filter(date__lt="", date__gt="").values(['amount']).sum()
for track in tracks:
            tl_data = Registration.objects.exclude(Q(is_staff=True) | Q(status__in=STATUSES_NOT)
                                                   ).filter(track=track).exclude(level='').values(
                'level').annotate(
                count=Count('level'),
                L=Sum(Case(
                    When(role='L', then=Value(1)),
                    default=0,
                    output_field=IntegerField(),
                )),
                F=Sum(Case(
                    When(role='F', then=Value(1)),
                    default=0,
                    output_field=IntegerField(),
                ))
                ,
                level2=Case(
                    When(level=Registration.BEGINNER,
                         then=Value(
                             Registration.LEVEL_CHOICES[1][1])),
                    When(
                        level=Registration.INTERMEDIATE,
                        then=Value(
                            Registration.LEVEL_CHOICES[
'''