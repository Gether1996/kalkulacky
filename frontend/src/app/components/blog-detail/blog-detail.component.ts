import { Component, OnInit, PLATFORM_ID, inject } from '@angular/core';
import { CommonModule, isPlatformBrowser } from '@angular/common';
import { ActivatedRoute, RouterLink } from '@angular/router';
import { DomSanitizer, SafeHtml } from '@angular/platform-browser';
import { BlogService } from '../../services/blog.service';
import { BlogPostDetail } from '../../models/blog.models';

@Component({
  selector: 'app-blog-detail',
  standalone: true,
  imports: [CommonModule, RouterLink],
  templateUrl: './blog-detail.component.html',
  styleUrls: ['./blog-detail.component.css']
})
export class BlogDetailComponent implements OnInit {
  private platformId = inject(PLATFORM_ID);
  
  post: BlogPostDetail | null = null;
  safeHtmlContent: SafeHtml | null = null;
  loading: boolean = true;
  error: string | null = null;

  constructor(
    private route: ActivatedRoute,
    private blogService: BlogService,
    private sanitizer: DomSanitizer
  ) {}

  ngOnInit() {
    if (isPlatformBrowser(this.platformId)) {
      const slug = this.route.snapshot.paramMap.get('slug');
      if (slug) {
        this.loadPost(slug);
      }
    }
  }

  loadPost(slug: string) {
    this.loading = true;
    this.error = null;
    
    this.blogService.getPost(slug).subscribe({
      next: (data) => {
        this.post = data;
        this.safeHtmlContent = this.sanitizer.bypassSecurityTrustHtml(data.content_html);
        this.loading = false;
      },
      error: (err) => {
        console.error('Error loading post:', err);
        this.error = 'Blog príspevok sa nenašiel';
        this.loading = false;
      }
    });
  }

  formatDate(dateString: string): string {
    const date = new Date(dateString);
    return date.toLocaleDateString('sk-SK', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    });
  }

  getCalculatorRoute(calculatorSlug: string): string {
    return `/calculator/${calculatorSlug}`;
  }
}
