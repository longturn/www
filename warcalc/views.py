from django import forms
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from django.template import Context, TemplateDoesNotExist
from django.template.loader import get_template
from longturn.warcalc.forms import *
from django.conf import settings
import datetime
from math import pow, floor
from tempfile import NamedTemporaryFile
from os import system

def warcalc(request):
	def remhp(atthp, defhp, attfp, deffp, attpo, defpo):
		p = float(attpo / float(defpo + attpo))
		k = int(floor(defhp / attfp))
		l = int(floor(atthp / deffp))

		def newt(n, k):
			l1 = 1
			for i in range(k + 1, n + 1):
				l1 *= i
			for i in range(1, n - k + 1):
				l1 /= i
			return l1

		x = 0
		f = NamedTemporaryFile(delete=True)
		# hp - hp lost in battle
		for hp in range(0, k):
			y = newt(hp + l, hp) * pow(p, hp) * pow(1 - p, l)
			f.write(b"%d %.20f\n" % (defhp - attfp * hp, y))
			x += y

		# defender lost
		# al - attacker loss of hitpoints
		y = 0
		for al in range(0, l):
			y += newt(k - 1 + al, al) * pow(p, k - 1) * pow(1 - p, al) * p
		x += y
		f.write(b"%d %.20f\n" % (0, y))
		f.flush()
		name = "%s/plots/warcalc/%s-%s-%s-%s-%s-%s.svg" % (settings.MEDIA_ROOT, atthp, defhp, attfp, deffp, attpo, defpo)
		system("gnuplot -e 'load \"%s/warcalc.p\"; set output \"%s\"; set ylabel \"probability\"; set xrange [0:%s]; plot \"%s\" with boxes linecolor rgb \"#000000\"' 2>/tmp/gnuplot_errors" % (settings.PLOT_PATH, name, atthp, f.name));
		f.close()
		return y

	
	if request.method == 'POST':
		form = WarCalcForm(request.POST)
		if form.is_valid():
			astr = float(request.POST['astr'])
			ahp = int(float(request.POST['ahp'])) # prevent stupid error if 20.0 supplied
			afp = int(float(request.POST['afp']))
			dstr = float(request.POST['dstr'])
			dhp = int(float(request.POST['dhp']))
			dfp = int(float(request.POST['dfp']))

			p = astr / (astr + dstr);
			def winprob(hp1, hp2, fp1, fp2):
				dp = [ [ 0.0 for i in range(hp2+1) ] for j in range(hp1+1) ]
				for i in range(hp1+1):
					for j in range(hp2+1):
						if i == 0:
							dp[i][j] = 0.0
							continue
						if j == 0:
							dp[i][j] = 1.0
							continue
						dp[i][j] = p * dp[max(0, i - fp2)][j] + (1.0 - p) * dp[i][max(0, j - fp1)]
				return 100.0 * dp[int(hp1)][int(hp2)]

			def exphp(lp, hp1, hp2, fp1, fp2):
				dh = [ [ 0.0 for i in range(hp2+1) ] for j in range(hp1+1) ]
				for i in range(hp1+1):
					for j in range(hp2+1):
						if i == 0:
							dh[i][j] = 0.0
							continue
						if j == 0:
							dh[i][j] = i
							continue
						dh[i][j] = lp * dh[max(0, i - fp2)][j] + (1.0 - lp) * dh[i][max(0, j - fp1)]
				return dh[int(hp1)][int(hp2)]

			tab = []
			ndhp = dhp
			for i in range(20):
				defprob = winprob(ndhp, ahp, dfp, afp)
				attprob = 100 - defprob
				dexphp = exphp(p, ndhp, ahp, dfp, afp)
				aexphp = exphp(1.0 - p, ahp, ndhp, afp, dfp)
				delta = ndhp - dexphp
				tab.append([attprob, aexphp, defprob, dexphp, delta])
				ndhp = int(dexphp)
				if ndhp == 0:
					break

			prob = remhp(ahp, dhp, afp, dfp, astr, dstr)
						
			form = WarCalcForm(initial={
				'astr': astr,
				'ahp': ahp,
				'afp': afp,
				'dstr': dstr,
				'dhp': dhp,
				'dfp': dfp,
			})
			return render(
                                request,
				'warcalc/warcalc.html',
				{
					'form': form,
					'tab': tab,
					'prob': "%.6f" % (prob * 100),
					'plot': "%s-%s-%s-%s-%s-%s.svg" % (ahp, dhp, afp, dfp, astr, dstr),
				})
	else:
		form = WarCalcForm(initial={
			'astr': 12.0,
			'ahp': 20,
			'afp': 1,
			'dstr': 4.5,
			'dhp': 20,
			'dfp': 1,
		})

	return render(
                request,
		'warcalc/warcalc.html',
		{
			'form': form,
		})

