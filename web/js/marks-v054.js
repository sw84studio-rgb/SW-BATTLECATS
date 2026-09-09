(()=>{'use strict';
const ROOT='../assets/common/marks/';
const TRAIT={
 '빨간 적':'e/0.png','떠있는 적':'e/1.png','검은 적':'e/2.png','메탈 적':'e/3.png','천사':'e/4.png','에이리언':'e/5.png',
 '좀비':'e/6.png','좀비 적':'e/6.png','고대종':'e/7.png','속성을 가지지 않은 적':'e/8.png','속성을 가지지 않는 적':'e/8.png',
 '사도':'e/9.png','마녀':'e/10.png','악마':'e/11.png','도장탑':'e/12.png','초수':'e/13.png','초생명체':'e/14.png','초현자':'e/15.png','괴인':'e/16.png'
};
const ABILITY={
 '공격력 업':'a/1.png','살아남는다':'a/2.png','성 파괴가 특기':'a/3.png','크리티컬':'a/4.png','좀비 킬러':'a/5.png','영혼 공격':'a/6.png',
 '베리어 브레이커':'a/7.png','쉴드 브레이커':'a/8.png','혼신의 일격':'a/9.png','격파시 머니 UP':'a/10.png','메탈':'a/11.png','소파동':'a/12.png',
 '파동공격':'a/13.png','파동 공격':'a/13.png','소열파':'a/14.png','열파 공격':'a/15.png','파동 스톱퍼':'a/16.png','초생명체 특효':'a/17.png',
 '초수 특효':'a/18.png','마녀 킬러':'a/19.png','사도 킬러':'a/20.png','공격력 다운':'a/21.png','움직임을 멈춘다':'a/22.png','움직임을 느리게 한다':'a/23.png',
 '공격 타겟의 한정':'a/24.png','엄청 강하다':'a/25.png','맷집이 좋다':'a/26.png','초 맷집이 좋다':'a/27.png','초 데미지':'a/28.png','극 데미지':'a/29.png',
 '날려버린다':'a/30.png','워프':'a/31.png','공격 무효':'a/32.png','저주':'a/33.png','고대의 저주':'a/33.png','지중 이동':'a/34.png','부활':'a/35.png',
 '독 공격':'a/36.png','베리어':'a/38.png','악마 쉴드':'a/39.png','열파 카운터':'a/40.png','데스 열파':'a/41.png','초현자 특효':'a/42.png',
 '소환':'a/43.png','메탈 킬러':'a/44.png','폭파 공격':'a/45.png','괴인 특효':'a/46.png','생산 지연':'a/47.png',
 '파동 데미지 무효':'m/0.png','움직임을 멈춘다 무효':'m/1.png','움직임을 느리게 한다 무효':'m/2.png','날려버린다 무효':'m/3.png',
 '열파 데미지 무효':'m/4.png','공격력 다운 무효':'m/5.png','워프 무효':'m/6.png','고대의 저주 무효':'m/7.png','저주 무효':'m/7.png',
 '독 데미지 무효':'m/8.png','마왕 진동 무효':'m/9.png','보스파동 무효':'m/9.png','폭파 데미지 무효':'m/10.png',
 '공격력 다운 내성':'r/0.png','정지 내성':'r/1.png','움직임을 멈춘다 내성':'r/1.png','느리게 내성':'r/2.png','움직임을 느리게 한다 내성':'r/2.png',
 '날려버리기 내성':'r/3.png','파동 내성':'r/4.png','열파 내성':'r/5.png','저주 내성':'r/6.png','독 내성':'r/7.png','워프 내성':'r/8.png'
};
function clean(s){return String(s??'').trim()}
function baseAbility(line){return clean(line).split(/\s*·\s*/,1)[0]}
function trait(label){const k=clean(label);const p=TRAIT[k];return p?{key:k,src:ROOT+p}:null}
function ability(line){const k=baseAbility(line);const p=ABILITY[k];return p?{key:k,src:ROOT+p}:null}
function splitTraits(value){return String(value??'').split(/\s*(?:·|,|\n)\s*/).map(clean).filter(Boolean)}
function splitAbilityLines(value){return String(value??'').split(/\n+/).map(clean).filter(Boolean)}
function splitResponses(value){return String(value??'').split(/\s*·\s*|\n+/).map(clean).filter(Boolean)}
window.SWBattleCatsMarksV054={trait,ability,baseAbility,splitTraits,splitAbilityLines,splitResponses,traitMap:Object.freeze({...TRAIT}),abilityMap:Object.freeze({...ABILITY})};
})();
