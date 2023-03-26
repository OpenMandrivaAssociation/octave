;; -*-emacs-lisp-*-
;;
;; Emacs startup file for the Mandrake GNU/Linux octave package
;;
;; Originally contributed by Nils Naumann <naumann@unileoben.ac.at>
;; Modified by Dirk Eddelbuettel <edd@debian.org>
;; Altered for Mandrake Linux by Thierry Vignaud <tvignaud@mandrakesoft.com>

;; The Octave mode calls this file
(autoload 'octave-mode "octave-mod" nil t)
(autoload 'octave-mode "octave-hlp" nil t)

(setq auto-mode-alist (cons '("\\.m$" . octave-mode) auto-mode-alist))
(add-hook 'octave-mode-hook
          (lambda ()
            (abbrev-mode 1)
            (auto-fill-mode 1)
            (if (eq window-system 'x)
		(font-lock-mode 1))))

(autoload 'run-octave "octave-inf" nil t)
(autoload 'inferior-octave "octave-inf" nil t)
(add-hook 'inferior-octave-mode-hook
          (lambda ()
            (turn-on-font-lock)
;            (define-key inferior-octave-mode-map [up]
;              'comint-previous-input)
;            (define-key inferior-octave-mode-map [down]
;              'comint-next-input)
	    ))

