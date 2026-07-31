import { Component, OnInit, PLATFORM_ID, DestroyRef, inject } from '@angular/core';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { CommonModule, isPlatformBrowser } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RouterModule } from '@angular/router';
import { AuthService } from '../../services/auth.service';
import { User } from '../../models/auth.models';
import { TranslatePipe } from '../../i18n/translate.pipe';
import { LocaleService } from '../../i18n/locale.service';
import {
  DashboardService, DashboardData, SavedCalculation, UpcomingNotification, DashboardStats, UserReminder,
  SavingsGoal,
} from '../../services/dashboard.service';
import { FavoritesService } from '../../services/favorites.service';
import { CALC_BY_ID, CalcMeta } from '../../config/calculator-registry';

@Component({
  selector: 'app-user-dashboard',
  imports: [CommonModule, FormsModule, RouterModule, TranslatePipe],
  templateUrl: './user-dashboard.html',
  styleUrl: './user-dashboard.css',
})
export class UserDashboard implements OnInit {
  private platformId = inject(PLATFORM_ID);
  private locale = inject(LocaleService);
  private dashboard = inject(DashboardService);
  favorites = inject(FavoritesService);
  private destroyRef = inject(DestroyRef);

  currentUser: User | null = null;
  accountCreatedDate: Date | null = null;

  loading = true;
  loadError = false;

  /** Transient error shown when a dashboard action (delete/save) fails. */
  actionError: string | null = null;

  private showActionError(): void {
    this.actionError = this.locale.t('common.actionError');
    setTimeout(() => (this.actionError = null), 5000);
  }

  stats: DashboardStats = {
    totalCalculations: 0,
    trackedCalculations: 0,
    favoritesCount: 0,
    upcomingNotifications: 0,
  };
  calculations: SavedCalculation[] = [];
  upcoming: UpcomingNotification[] = [];
  reminders: UserReminder[] = [];
  savingsGoals: SavingsGoal[] = [];

  // New-goal form
  showGoalForm = false;
  goalSaving = false;
  newGoal = { name: '', target_amount: null as number | null, initial_amount: 0,
              monthly_contribution: 0, annual_rate: 0, target_date: '' };

  // Add-deposit form (per goal)
  depositGoalId: number | null = null;
  depositSaving = false;
  newDeposit = { amount: null as number | null, date: '', note: '' };

  // New-reminder form
  newReminder = { title: '', remind_date: '', note: '', category: 'custom', frequency: 'once' };
  reminderSaving = false;

  reminderFrequencies = ['once', 'daily', 'weekly', 'monthly', 'yearly'];

  // Inline note editing on saved calculations
  editingNoteId: number | null = null;
  noteDraft = '';

  // Inline reminder editing
  editingReminderId: number | null = null;
  reminderEdit = { title: '', remind_date: '', note: '' };

  // One-click SK/CZ financial-deadline presets (relative offsets resolved on click).
  reminderPresets = [
    { key: 'tax', titleKey: 'dash.preset.tax', month: 3, day: 31, category: 'tax' },
    { key: 'szco', titleKey: 'dash.preset.szco', month: 1, day: 31, category: 'tax' },
    { key: 'pzp', titleKey: 'dash.preset.pzp', month: 0, day: 0, category: 'insurance' },
  ];

  // Quick links to the highest-value calculators (names resolved via i18n).
  popularCalculators = [
    { id: 'salary', route: '/calculator/salary', icon: '💰' },
    { id: 'mortgage', route: '/calculator/mortgage', icon: '🏠' },
    { id: 'heat-pump', route: '/calculator/heat-pump', icon: '♨️' },
    { id: 'solar', route: '/calculator/solar', icon: '☀️' },
    { id: 'renovation', route: '/calculator/renovation', icon: '🏚️' },
    { id: 'pension', route: '/calculator/pension', icon: '💼' },
  ];

  constructor(private authService: AuthService) {}

  ngOnInit() {
    this.authService.currentUser$
      .pipe(takeUntilDestroyed(this.destroyRef))
      .subscribe(user => {
      this.currentUser = user;
      if (user && (user as any).date_joined) {
        this.accountCreatedDate = new Date((user as any).date_joined);
      }
    });
    if (isPlatformBrowser(this.platformId)) {
      this.loadDashboard();
    }
  }

  loadDashboard() {
    this.loading = true;
    this.loadError = false;
    this.dashboard.getDashboard().subscribe({
      next: (data: DashboardData) => {
        this.stats = data.stats;
        this.calculations = data.calculations ?? [];
        this.upcoming = data.upcomingNotifications ?? [];
        this.reminders = data.reminders ?? [];
        this.savingsGoals = data.savingsGoals ?? [];
        this.loading = false;
      },
      error: () => {
        this.loadError = true;
        this.loading = false;
      },
    });
  }

  toggleFavorite(calc: SavedCalculation) {
    const next = !calc.is_favorite;
    calc.is_favorite = next;
    this.dashboard.updateCalculation(calc.id, { is_favorite: next }).subscribe({
      next: () => this.recomputeStats(),
      error: () => { calc.is_favorite = !next; },
    });
  }

  toggleTracking(calc: SavedCalculation) {
    const next = !calc.is_tracking;
    calc.is_tracking = next;
    this.dashboard.updateCalculation(calc.id, { is_tracking: next }).subscribe({
      next: () => this.loadDashboard(),
      error: () => { calc.is_tracking = !next; },
    });
  }

  remove(calc: SavedCalculation) {
    this.dashboard.deleteCalculation(calc.id).subscribe({
      next: () => {
        this.calculations = this.calculations.filter(c => c.id !== calc.id);
        this.recomputeStats();
      },
      error: () => this.showActionError(),
    });
  }

  // ---- Custom reminders ----
  addReminder() {
    const title = this.newReminder.title.trim();
    if (!title || !this.newReminder.remind_date) return;
    this.reminderSaving = true;
    this.dashboard.createReminder({
      title,
      remind_date: this.newReminder.remind_date,
      note: this.newReminder.note || '',
      category: this.newReminder.category || 'custom',
      frequency: (this.newReminder.frequency || 'once') as any,
    }).subscribe({
      next: (res) => {
        if (res.success) {
          this.reminders = [...this.reminders, res.data]
            .sort((a, b) => a.remind_date.localeCompare(b.remind_date));
          this.newReminder = { title: '', remind_date: '', note: '', category: 'custom', frequency: 'once' };
          this.stats = { ...this.stats, upcomingNotifications: this.stats.upcomingNotifications + 1 };
        }
        this.reminderSaving = false;
      },
      error: () => { this.reminderSaving = false; },
    });
  }

  applyPreset(p: { titleKey: string; month: number; day: number; category: string }) {
    const now = new Date();
    let target: Date;
    if (p.month === 0) {
      // No fixed date (e.g. PZP renewal) → default one month out.
      target = new Date(now.getFullYear(), now.getMonth() + 1, now.getDate());
    } else {
      target = new Date(now.getFullYear(), p.month - 1, p.day);
      if (target < now) target = new Date(now.getFullYear() + 1, p.month - 1, p.day);
    }
    this.newReminder = {
      title: this.locale.t(p.titleKey),
      remind_date: this.toISODate(target),
      note: '',
      category: p.category,
      frequency: 'once',
    };
  }

  removeReminder(r: UserReminder) {
    this.dashboard.deleteReminder(r.id).subscribe({
      next: () => {
        this.reminders = this.reminders.filter(x => x.id !== r.id);
        this.stats = { ...this.stats, upcomingNotifications: Math.max(0, this.stats.upcomingNotifications - 1) };
      },
      error: () => this.showActionError(),
    });
  }

  startEditReminder(r: UserReminder) {
    this.editingReminderId = r.id;
    this.reminderEdit = { title: r.title, remind_date: r.remind_date, note: r.note || '' };
  }

  saveReminderEdit(r: UserReminder) {
    const patch = {
      title: this.reminderEdit.title.trim(),
      remind_date: this.reminderEdit.remind_date,
      note: this.reminderEdit.note,
    };
    if (!patch.title || !patch.remind_date) return;
    this.dashboard.updateReminder(r.id, patch).subscribe({
      next: (res) => {
        if (res.success) {
          Object.assign(r, res.data);
          this.reminders = [...this.reminders].sort((a, b) => a.remind_date.localeCompare(b.remind_date));
        }
        this.editingReminderId = null;
      },
      error: () => { this.editingReminderId = null; },
    });
  }

  cancelEditReminder() { this.editingReminderId = null; }

  private toISODate(d: Date): string {
    return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`;
  }

  // ---- Notes on saved calculations ----
  startEditNote(calc: SavedCalculation) {
    this.editingNoteId = calc.id;
    this.noteDraft = calc.note || '';
  }

  saveNote(calc: SavedCalculation) {
    const note = this.noteDraft;
    this.dashboard.updateCalculation(calc.id, { note }).subscribe({
      next: () => { calc.note = note; this.editingNoteId = null; },
      error: () => { this.editingNoteId = null; },
    });
  }

  cancelNote() { this.editingNoteId = null; }

  // ---- Export ----
  exportCsv() {
    if (!isPlatformBrowser(this.platformId)) return;
    const esc = (v: any) => `"${String(v ?? '').replace(/"/g, '""')}"`;
    const rows: string[] = [];
    rows.push(['Typ', 'Názov', 'Dátum', 'Poznámka'].map(esc).join(','));
    for (const c of this.calculations) {
      rows.push([c.calculator_type_display || c.calculator_type, c.name,
                 this.formatDate(c.created_at || null), c.note || ''].map(esc).join(','));
    }
    for (const r of this.reminders) {
      rows.push(['Pripomienka', r.title, this.formatDate(r.remind_date), r.note || ''].map(esc).join(','));
    }
    const blob = new Blob(['﻿' + rows.join('\r\n')], { type: 'text/csv;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'kalkulacky-export.csv';
    a.click();
    URL.revokeObjectURL(url);
  }

  printPdf() {
    if (!isPlatformBrowser(this.platformId)) return;
    const t = (k: string) => this.locale.t(k);
    const rowsCalc = this.calculations.map(c =>
      `<tr><td>${this.escapeHtml(c.calculator_type_display || c.calculator_type)}</td>` +
      `<td>${this.escapeHtml(c.name)}</td><td>${this.formatDate(c.created_at || null)}</td>` +
      `<td>${this.escapeHtml(c.note || '')}</td></tr>`).join('');
    const rowsRem = this.reminders.map(r =>
      `<tr><td>🔔</td><td>${this.escapeHtml(r.title)}</td><td>${this.formatDate(r.remind_date)}</td>` +
      `<td>${this.escapeHtml(r.note || '')}</td></tr>`).join('');
    const html = `<!doctype html><html><head><meta charset="utf-8">
      <title>${t('dash.title')} — Kalkulačky.sk</title>
      <style>body{font-family:Arial,sans-serif;padding:24px;color:#1e293b}
      h1{font-size:20px}h2{font-size:15px;margin-top:20px}
      table{width:100%;border-collapse:collapse;font-size:13px;margin-top:8px}
      th,td{border:1px solid #e2e8f0;padding:7px 10px;text-align:left}
      th{background:#f8fafc}</style></head><body>
      <h1>${t('dash.title')}</h1>
      <h2>${t('dash.saved.title')}</h2>
      <table><thead><tr><th>${t('dash.action.note')}</th><th>${t('save.nameLabel')}</th><th>${t('dash.memberSince')}</th><th>${t('dash.action.note')}</th></tr></thead><tbody>${rowsCalc || '<tr><td colspan="4">—</td></tr>'}</tbody></table>
      <h2>${t('dash.myReminders.title')}</h2>
      <table><thead><tr><th></th><th>${t('dash.myReminders.titlePh')}</th><th>${t('dash.memberSince')}</th><th>${t('dash.action.note')}</th></tr></thead><tbody>${rowsRem || '<tr><td colspan="4">—</td></tr>'}</tbody></table>
      <script>window.onload=function(){window.print();}</script></body></html>`;
    const w = window.open('', '_blank');
    if (w) { w.document.write(html); w.document.close(); }
  }

  private escapeHtml(s: string): string {
    return (s || '').replace(/[&<>"]/g, ch =>
      ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' } as Record<string, string>)[ch]);
  }

  private recomputeStats() {
    this.stats = {
      ...this.stats,
      totalCalculations: this.calculations.length,
      trackedCalculations: this.calculations.filter(c => c.is_tracking).length,
      favoritesCount: this.calculations.filter(c => c.is_favorite).length,
    };
  }

  // ---- Favorite tools ("My tools") ----
  get myTools(): CalcMeta[] {
    return this.favorites.favorites()
      .map(f => CALC_BY_ID[f.calculator_id])
      .filter((c): c is CalcMeta => !!c);
  }

  toolName(id: string): string {
    return this.locale.t('calc.' + id + '.name');
  }

  moveTool(index: number, dir: -1 | 1) {
    const ids = this.myTools.map(t => t.id);
    const target = index + dir;
    if (target < 0 || target >= ids.length) return;
    [ids[index], ids[target]] = [ids[target], ids[index]];
    this.favorites.reorder(ids);
  }

  removeTool(id: string) {
    this.favorites.remove(id);
  }

  // ---- Savings goals ----
  openGoalForm() {
    this.showGoalForm = true;
    this.newGoal = { name: '', target_amount: null, initial_amount: 0,
                     monthly_contribution: 0, annual_rate: 0, target_date: '' };
  }

  cancelGoalForm() { this.showGoalForm = false; }

  addGoal() {
    const name = this.newGoal.name.trim();
    if (!name || !this.newGoal.target_amount) return;
    this.goalSaving = true;
    this.dashboard.createSavingsGoal({
      name,
      target_amount: this.newGoal.target_amount,
      initial_amount: this.newGoal.initial_amount || 0,
      monthly_contribution: this.newGoal.monthly_contribution || 0,
      annual_rate: this.newGoal.annual_rate || 0,
      target_date: this.newGoal.target_date || null,
      currency: this.goalCurrency(),
    }).subscribe({
      next: (res) => {
        if (res.success) {
          this.savingsGoals = [res.data, ...this.savingsGoals];
          this.showGoalForm = false;
        }
        this.goalSaving = false;
      },
      error: () => { this.goalSaving = false; },
    });
  }

  removeGoal(goal: SavingsGoal) {
    if (isPlatformBrowser(this.platformId) && !confirm(this.locale.t('dash.sg.deleteConfirm'))) return;
    this.dashboard.deleteSavingsGoal(goal.id).subscribe({
      next: () => { this.savingsGoals = this.savingsGoals.filter(g => g.id !== goal.id); },
      error: () => this.showActionError(),
    });
  }

  openDeposit(goal: SavingsGoal) {
    this.depositGoalId = goal.id;
    this.newDeposit = { amount: null, date: this.toISODate(new Date()), note: '' };
  }

  cancelDeposit() { this.depositGoalId = null; }

  addDeposit(goal: SavingsGoal) {
    if (!this.newDeposit.amount || !this.newDeposit.date) return;
    this.depositSaving = true;
    this.dashboard.addContribution(goal.id, {
      amount: this.newDeposit.amount,
      date: this.newDeposit.date,
      note: this.newDeposit.note || '',
    }).subscribe({
      next: (res) => {
        if (res.success) {
          // Replace the goal with the refreshed copy (progress recomputed server-side).
          this.savingsGoals = this.savingsGoals.map(g => g.id === goal.id ? res.data : g);
          this.depositGoalId = null;
        }
        this.depositSaving = false;
      },
      error: () => { this.depositSaving = false; },
    });
  }

  goalRemaining(goal: SavingsGoal): number {
    return Math.max(0, goal.target_amount - goal.current_balance);
  }

  goalStatusKey(goal: SavingsGoal): string {
    return 'dash.sg.status.' + (goal.progress?.status ?? 'no_deadline');
  }

  /** Currency for a NEW goal follows the active language. */
  private goalCurrency(): string {
    const map: Record<string, string> = { sk: 'EUR', cs: 'CZK', en: 'EUR', pl: 'PLN', hu: 'HUF' };
    return map[this.locale.locale()] ?? 'EUR';
  }

  formatGoalCurrency(value: number | null | undefined, currency: string): string {
    if (value == null) return '—';
    const localeMap: Record<string, string> = {
      EUR: 'sk-SK', CZK: 'cs-CZ', PLN: 'pl-PL', HUF: 'hu-HU',
    };
    try {
      return new Intl.NumberFormat(localeMap[currency] ?? 'sk-SK', {
        style: 'currency', currency, maximumFractionDigits: 0,
      }).format(value);
    } catch {
      return `${Math.round(value)} ${currency}`;
    }
  }

  getUserInitials(): string {
    if (!this.currentUser) return '';
    if (this.currentUser.first_name && this.currentUser.last_name) {
      return `${this.currentUser.first_name[0]}${this.currentUser.last_name[0]}`.toUpperCase();
    }
    if (this.currentUser.first_name) return this.currentUser.first_name.substring(0, 2).toUpperCase();
    if (this.currentUser.email) return this.currentUser.email.substring(0, 2).toUpperCase();
    return 'U';
  }

  getUserDisplayName(): string {
    if (!this.currentUser) return '';
    if (this.currentUser.first_name && this.currentUser.last_name) {
      return `${this.currentUser.first_name} ${this.currentUser.last_name}`;
    }
    if (this.currentUser.first_name) return this.currentUser.first_name;
    return this.currentUser.email;
  }

  formatDate(value: Date | string | null): string {
    if (!value) return '—';
    const date = typeof value === 'string' ? new Date(value) : value;
    if (isNaN(date.getTime())) return '—';
    return new Intl.DateTimeFormat(this.locale.locale(), {
      year: 'numeric', month: 'long', day: 'numeric',
    }).format(date);
  }
}
