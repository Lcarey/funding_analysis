%% read abstracts
DS = dataset('file','word_counts.tab');

DS.frac = NaN(length(DS),1);
for I = 1:length(years)
    idx = DS.year == years(I);
    DS.frac(idx) = DS.count(idx) ./ sum(DS.count(idx));
end
years = unique(DS.year);

%% which terms are monontonically increasing or decreasing?
R=dataset();
R.unique_words = unique(DS.word( DS.frac > 1e-6 )) ;
for I = 1:length(unique_words)
    idx = strcmp(DS.word,unique_words{I});
    [R.C(I) , R.P(I)] = corr(DS.year(idx)  , DS.frac( idx));
end
R = R( R.P<0.001 , :);
R = sortrows(R,'C','ascend');

%%
words = {'maize' 'arabidopsis'  'tomato' 'soy' 'zebrafish'};
%words = {'rat' 'coli' 'mouse' 'arabidopsis' 'maize' };
%words = {'feces' 'fecal' 'microbiota'}
clrs = hsv(length(words));
figure; hold on; grid on;
for  I = 1:length(words)
    idx = strcmp(DS.word,words{I}) ; 
    Y = DS.count(idx ) ;
    X = 
 %   plot(DS.year( idx) , DS.frac(idx )-DS.frac(idx & DS.year==1985 ) , '-' ,'Color',clrs(I,:),'DisplayName',words{I},'LineWidth',3);
    plot(DS.year( idx) , Y , '-' ,'Color',clrs(I,:),'DisplayName',words{I},'LineWidth',3);

end
%line(xlim,[0 0],'LineStyle','--','Color','k');
%ylim([0 3e-5])
legend('location','ne');
xlabel('year')
ylabel('fraction of words / year')
set(gcf,'PaperPosition',[0 0 6 4])
print('-dpng','NIH.png')

